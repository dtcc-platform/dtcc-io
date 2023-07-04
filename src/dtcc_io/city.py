# Copyright (C) 2022 Dag Wästberg
# Licensed under the MIT License

# %%
import json
from pathlib import Path

import shapely.geometry
import shapely.ops
import shapely.affinity
import fiona
import pyproj

from . import generic

# from dtcc_model import Polygon, Building, LinearRing, Vector2D, City
import dtcc_model as model
from dtcc_model.building import Building
from dtcc_model.geometry import Bounds
from dtcc_model.city import City
from .logging import info, warning, error


def building_bounds(shp_footprint_file, buffer=0):
    """calculate the bounding box of a shp file without loading it"""
    with fiona.open(shp_footprint_file) as c:
        bbox = Bounds(*c.bounds)
    bbox.buffer(buffer)
    return bbox


# %%


def cleanLinearRing(coords, tol=0.1):
    # s = shapely.geometry.Polygon(coords)
    # s = shapely.geometry.Polygon.orient(s, 1)  # make ccw
    # s = s.simplify(tol)
    # return list(s.exterior.coords)[:-1]
    return coords


def _building_from_fiona(s, uuid_field="id", height_field=""):
    building = Building()
    if uuid_field in s["properties"]:
        building.uuid = str(s["properties"][uuid_field])
    if height_field in s["properties"] and s["properties"][height_field]:
        try:
            building.height = float(s["properties"][height_field])
        except ValueError:
            print(f"Error cannot parse height field: {s['properties'][height_field]}")

    building.footprint = shapely.geometry.shape(s["geometry"])
    building.attributes = s["properties"]
    return building


def _load_proto_city(filename):
    city = City()
    city.from_proto(filename.read_bytes())
    return city


def _load_fiona(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds=None,
    min_edge_distance=2.0,
):
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    city = City()
    buildings = []
    has_height_field = len(height_field) > 0
    bounds_filter = None
    if bounds is not None:
        city.bounds = bounds
        bounds_filter = shapely.geometry.box(*bounds.tuple).buffer(-min_edge_distance)
    try:
        f = fiona.open(filename)
        f.close()
    except fiona.errors.DriverError:
        raise ValueError(f"File {filename} is not a valid file format")
    info(f"Loading city from {filename}")
    with fiona.open(filename) as src:
        crs = src.crs["init"]
        for s in src:
            if area_filter is not None and area_filter > 0:
                if shapely.geometry.shape(s["geometry"]).area < area_filter:
                    continue
            if bounds_filter is not None:
                if not shapely.geometry.shape(s["geometry"]).intersects(bounds_filter):
                    continue
            geom_type = s["geometry"]["type"]
            if geom_type == "Polygon":
                building = _building_from_fiona(s, uuid_field, height_field)
                buildings.append(building)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(
                    list(shapely.geometry.shape(s["geometry"]).geoms)
                ):
                    # make each polygon its own building
                    building = _building_from_fiona(s, uuid_field, height_field)
                    if len(building.uuid) > 0:
                        building.uuid = f"{building.uuid}_{idx}"
                    building.footprint = polygon
                    buildings.append(building)

    city.buildings = buildings
    city.crs = crs
    if bounds is not None:
        if isinstance(bounds, model.Bounds):
            city.bounds = bounds
        else:
            city.bounds = model.Bounds(
                xmin=bounds[0], ymin=bounds[1], xmax=bounds[2], ymax=bounds[3]
            )
    else:
        # calculate bounds
        for b in city.buildings:
            bbounds = model.Bounds(*b.footprint.bounds)
            city.bounds.union(bbounds)
        city.bounds.buffer(min_edge_distance)
    return city


def load(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds=None,
    min_edge_distance=2.0,
):
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    return generic.load(
        filename,
        "city",
        City,
        _load_formats,
        uuid_field=uuid_field,
        height_field=height_field,
        area_filter=area_filter,
        bounds=bounds,
        min_edge_distance=min_edge_distance,
    )


def _save_proto_city(city, filename):
    with open(filename, "wb") as dst:
        dst.write(city.to_proto().SerializeToString())


def _save_json_city(city, filename):
    with open(filename, "w") as dst:
        dst.write(city.to_json())


def _save_fiona(city, out_file, output_format=""):
    offset = city.origin
    out_file = Path(out_file)
    output_format = out_file.suffix.lower()
    driver = {
        ".shp": "ESRI Shapefile",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".gpkg": "GPKG",
    }
    crs = city.crs
    if not crs:
        crs = "EPSG:3006"  # current dtcc default
    if driver[output_format] == "GeoJSON" and crs:
        # geojson needs to be in lat/lon
        wgs84 = pyproj.CRS("EPSG:4326")
        cm_crs = pyproj.CRS(crs)
        wgs84_projection = pyproj.Transformer.from_crs(cm_crs, wgs84, always_xy=True)
        crs = "EPSG:4326"
    schema = {
        "geometry": "Polygon",
        "properties": {
            "id": "str",
            "height": "float",
            "ground_height": "float",
            "error": "int",
        },
    }
    with fiona.open(out_file, "w", driver[output_format], schema, crs=crs) as dst:
        for building in city.buildings:
            shapely_footprint = building.footprint
            shapely_footprint = shapely.affinity.translate(
                shapely_footprint, xoff=offset[0], yoff=offset[1]
            )
            if driver[output_format] == "GeoJSON":
                shapely_footprint = shapely.ops.transform(
                    wgs84_projection.transform, shapely_footprint
                )
            dst.write(
                {
                    "geometry": shapely.geometry.mapping(shapely_footprint),
                    "properties": {
                        "id": building.uuid,
                        "height": building.height,
                        "ground_height": building.ground_level,
                        "error": building.error,
                    },
                }
            )


def save(city, filename):
    generic.save(city, filename, "city", _save_formats)


def list_io():
    return generic.list_io("city", _load_formats, _save_formats)


def print_io():
    generic.print_io("city", _load_formats, _save_formats)


_load_formats = {
    City: {
        ".pb": _load_proto_city,
        ".pb2": _load_proto_city,
        ".json": _load_fiona,
        ".shp": _load_fiona,
        ".geojson": _load_fiona,
        ".gpkg": _load_fiona,
    }
}

_save_formats = {
    City: {
        ".pb": _save_proto_city,
        ".pb2": _save_proto_city,
        ".json": _save_json_city,
        ".shp": _save_fiona,
        ".geojson": _save_fiona,
        ".gpkg": _save_fiona,
    }
}
