# Copyright (C) 2023 Dag Wästberg
# Licensed under the MIT License

from pathlib import Path
import shapely.geometry
import shapely.ops
import shapely.affinity
import fiona
from typing import Tuple, Callable
import numpy as np
import pyproj

from dtcc_model.roadnetwork import RoadNetwork, RoadType, Road
from dtcc_model.geometry import Georef
from . import generic
from .logging import info, warning, error

from enum import Enum, auto


class RoadDatasource(Enum):
    LM = auto()
    OSM = auto()
    NONE = auto()


def lm_road_type_mapping(category) -> Tuple[RoadType, bool, bool]:
    category = category.strip()
    split_category = category.split(",")
    base_type = split_category[0]

    tunnel = False
    bridge = False
    if "tunnel" in category:
        tunnel = True
    if "bro" in category:
        bridge = True

    if base_type == "Gata":
        if "större" in category:
            road_type = RoadType.SECONDARY
            return road_type, tunnel, bridge
        else:
            road_type = RoadType.RESIDENTIAL
            return road_type, tunnel, bridge

    if "cykel" in category:
        road_type = RoadType.CYCLEWAY
        return road_type, tunnel, bridge
    if "gång" in category:
        road_type = RoadType.FOOTWAY
        return road_type, tunnel, bridge

    if base_type == "Allmän väg < 5 m":
        road_type = RoadType.TERTIARY
        return road_type, tunnel, bridge
    if base_type == "Allmän väg > 7 m":
        road_type = RoadType.PRIMARY
        return road_type, tunnel, bridge

    if base_type == "Motorväg":
        road_type = RoadType.MOTORWAY
        return road_type, tunnel, bridge

    if base_type == "På- och avfartsväg":
        road_type = RoadType.PRIMARY
        return road_type, tunnel, bridge

    if base_type == "Bilväg":
        road_type = RoadType.SECONDARY
        return road_type, tunnel, bridge

    if "Sämre bilväg" in category:
        road_type = RoadType.TERTIARY
        return road_type, tunnel, bridge

    return None, tunnel, bridge


TV_ROAD_TYPE = {}


road_attribute_mappings = {
    RoadDatasource.LM: lm_road_type_mapping,
    RoadDatasource.OSM: None,
    RoadDatasource.NONE: lambda x: (RoadType.PRIMARY, False, False),
}


def _load_proto_roadnetwork(filename):
    road_network = RoadNetwork()
    road_network.from_proto(filename.read_bytes())
    return road_network


def _load_fiona(
    filename,
    type_field="KATEGORI",
    name_field="NAMN",
    road_datasource: RoadDatasource = RoadDatasource.LM,
    road_attribute_mapping_fn: Callable[[str], Tuple[RoadType, bool, bool]] = None,
    simplify: float = 0,
    **kwargs,
):
    filename = Path(filename)

    if road_attribute_mapping_fn is None:
        road_attribute_mapping_fn = road_attribute_mappings.get(road_datasource)
    if road_attribute_mapping_fn is None:
        warning(f"Road attribute mapping function not found, using default")
        road_attribute_mapping_fn = road_attribute_mapping_fn[RoadDatasource.NONE]

    road_network = RoadNetwork()
    roads = []

    vertex_map = {}

    with fiona.open(filename, "r") as src:
        crs = src.crs["init"]
        for s in src:
            if s["geometry"]["type"] != "LineString":
                continue
            road_type, tunnel, bridge = road_attribute_mapping_fn(
                s["properties"][type_field]
            )
            if road_type is None:
                warning(
                    f'Unknown road type: {s["properties"][type_field]}, using default'
                )
                road_type = RoadType.PRIMARY
            road_geometry = shapely.geometry.shape(s["geometry"])
            if simplify > 0:
                road_geometry = road_geometry.simplify(simplify, preserve_topology=True)
            road = Road()
            road.road_geometry = road_geometry
            road.road_type = road_type
            road.tunnel = tunnel
            road.bridge = bridge
            road.road_name = s["properties"].get(name_field, "")

            for v in road.road_geometry.coords:
                v = (round(v[0], 3), round(v[1], 3))
                if v not in vertex_map:
                    vertex_map[v] = len(vertex_map)
                road.road_vertices.append(vertex_map[v])
            roads.append(road)
        road_network.roads = roads
        road_network.georef = Georef(crs=str(crs))
        road_network.vertices = np.array([[v[0], v[1]] for v in vertex_map.keys()])
    return road_network


def load(
    road_network_file,
    type_field="KATEGORI",
    name_field="NAMN",
    road_datasource: RoadDatasource = RoadDatasource.LM,
    road_attribute_mapping_fn: Callable[[str], Tuple[RoadType, bool, bool]] = None,
    simplify: float = 0,
) -> RoadNetwork:
    road_network_file = Path(road_network_file)
    return generic.load(
        road_network_file,
        "roadnetwork",
        RoadNetwork,
        _load_formats,
        type_field=type_field,
        name_field=name_field,
        road_datasource=road_datasource,
        road_attribute_mapping_fn=road_attribute_mapping_fn,
        simplify=simplify,
    )


def _save_proto_roadnetwork(road_network: RoadNetwork, out_file: Path):
    out_file.write_bytes(road_network.to_proto().SerializeToString())
    return True


def _save_fiona(road_network: RoadNetwork, out_file: str):
    output_format = out_file.suffix
    driver = {
        ".shp": "ESRI Shapefile",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".gpkg": "GPKG",
    }
    if output_format not in driver:
        error(f"Unable to save road network; format {output_format} not supported")
    crs = road_network.georef.crs
    if not crs:
        crs = "EPSG:3006"  # current dtcc default

    if driver[output_format] == "GeoJSON" and crs:
        # geojson needs to be in lat/lon
        wgs84 = pyproj.CRS("EPSG:4326")
        cm_crs = pyproj.CRS(crs)
        wgs84_projection = pyproj.Transformer.from_crs(cm_crs, wgs84, always_xy=True)
        crs = "EPSG:4326"

    schema = {
        "geometry": "LineString",
        "properties": {
            "id": "str",
            "roadname": "str",
            "roadtype": "str",
            "roadwidth": "float",
            "tunnel": "bool",
            "bridge": "bool",
            "lanes": "int",
        },
    }
    with fiona.open(out_file, "w", driver[output_format], schema, crs=crs) as dst:
        for road in road_network.roads:
            road_geometry = road.road_geometry
            if driver[output_format] == "GeoJSON":
                road_geometry = shapely.ops.transform(
                    wgs84_projection.transform, road_geometry
                )
            dst.write(
                {
                    "geometry": shapely.geometry.mapping(road_geometry),
                    "properties": {
                        "id": road.road_id,
                        "roadname": road.road_name,
                        "roadtype": road.road_type.name.lower(),
                        "roadwidth": road.road_width,
                        "tunnel": road.tunnel,
                        "bridge": road.bridge,
                        "lanes": road.lanes,
                    },
                }
            )
    return True


def save(road_network: RoadNetwork, out_file):
    out_file = Path(out_file)
    return generic.save(road_network, out_file, "roadnetwork", _save_formats)


def list_io():
    return generic.list_io("roadnetwork", _load_formats, _save_formats)


def print_io():
    generic.print_io("roadnetwork", _load_formats, _save_formats)


_load_formats = {
    RoadNetwork: {
        ".pb": _load_proto_roadnetwork,
        ".pb2": _load_proto_roadnetwork,
        ".shp": _load_fiona,
        ".geojson": _load_fiona,
        ".json": _load_fiona,
        ".gpkg": _load_fiona,
    }
}

_save_formats = {
    RoadNetwork: {
        ".pb": _save_proto_roadnetwork,
        ".pb2": _save_proto_roadnetwork,
        ".shp": _save_fiona,
        ".geojson": _save_fiona,
    }
}
