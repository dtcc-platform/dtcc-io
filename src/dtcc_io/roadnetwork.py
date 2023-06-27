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
from .logging import info, warning, error


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


def load(
    road_network_file,
    type_field="KATEGORI",
    type_map: Callable[[str], Tuple[RoadType, bool, bool]] = lm_road_type_mapping,
    name_field="NAMN",
    simplify: float = 0,
) -> RoadNetwork:
    info(f"Loading road network from {road_network_file}")
    filename = Path(road_network_file)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")

    road_network = RoadNetwork()
    if filename.suffix.lower() in [".pb", ".pb2"]:
        road_network.from_proto(filename.read_bytes())
        return road_network
    roads = []

    vertex_map = {}

    with fiona.open(filename, "r") as src:
        crs = src.crs["init"]
        for s in src:
            if s["geometry"]["type"] != "LineString":
                continue
            road_type, tunnel, bridge = type_map(s["properties"][type_field])
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


def save(road_network: RoadNetwork, out_file: str):
    info(f"Saving road network to {out_file}")
    out_file = Path(out_file)
    output_format = out_file.suffix
    supported_formats = [".shp", ".json", ".geojson", ".gpkg", ".pb", ".pb2"]
    if not output_format in supported_formats:
        print(
            f"Error! Format {output_format} not recognized, currently supported formats are: {supported_formats}"
        )
        return None
    if output_format == ".pb" or output_format == ".pb2":
        with open(out_file, "wb") as dst:
            dst.write(road_network.to_proto().SerializeToString())
        return True
    driver = {
        ".shp": "ESRI Shapefile",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".gpkg": "GPKG",
    }
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
