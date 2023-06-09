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

from .utils import protobuf_to_json

# from dtcc_model import Polygon, Building, LinearRing, Vector2D, CityModel
import dtcc_model as model
from dtcc_model.building import Building
from dtcc_model.citymodel import CityModel
from .dtcc_logging import info, error


def building_bounds(shp_footprint_file, buffer=0):
    """calculate the bounding box of a shp file without loading it"""
    with fiona.open(shp_footprint_file) as c:
        bbox = c.bounds
    if buffer != 0:
        px, py, qx, qy = bbox
        bbox = (px - buffer, py - buffer, qx + buffer, qy + buffer)
    return bbox


# %%


def cleanLinearRing(coords, tol=0.1):
    # s = shapely.geometry.Polygon(coords)
    # s = shapely.geometry.Polygon.orient(s, 1)  # make ccw
    # s = s.simplify(tol)
    # return list(s.exterior.coords)[:-1]
    return coords


def building_from_fiona(s, uuid_field="id", height_field=""):
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


def load(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds=None,
    min_edge_distance=2.0,
    return_serialized=False,
):
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    cityModel = CityModel()
    if filename.suffix.lower() in [".pb", ".pb2"]:
        cityModel.from_proto(filename.read_bytes())
        return cityModel
    buildings = []
    has_height_field = len(height_field) > 0
    bounds_filter = None
    if bounds is not None:
        cityModel.bounds = bounds
        bounds_filter = shapely.geometry.box(*bounds.tuple).buffer(-min_edge_distance)
    try:
        f = fiona.open(filename)
        f.close()
    except fiona.errors.DriverError:
        raise ValueError(f"File {filename} is not a valid file format")
    info(f"Loading citymodel from {filename}")
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
                building = building_from_fiona(s, uuid_field, height_field)
                buildings.append(building)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(
                    list(shapely.geometry.shape(s["geometry"]).geoms)
                ):
                    # make each polygon its own building
                    building = building_from_fiona(s, uuid_field, height_field)
                    if len(building.uuid) > 0:
                        building.uuid = f"{building.uuid}_{idx}"
                    building.footprint = polygon
                    buildings.append(building)

    cityModel.buildings = buildings
    cityModel.crs = crs
    if bounds is not None:
        if isinstance(bounds, model.Bounds):
            cityModel.bounds = bounds
        else:
            cityModel.bounds = model.Bounds(
                xmin=bounds[0], ymin=bounds[1], xmax=bounds[2], ymax=bounds[3]
            )
    else:
        # calculate bounds
        for b in cityModel.buildings:
            bbounds = model.Bounds(*b.footprint.bounds)
            cityModel.bounds.union(bbounds)
        cityModel.bounds.buffer(min_edge_distance)
    return cityModel


def save(city_model, out_file, output_format=""):
    offset = city_model.origin
    out_file = Path(out_file)
    if output_format == "":
        output_format = out_file.suffix.lower()
    if not output_format.startswith("."):
        output_format = "." + output_format
    supported_formats = [".shp", ".json", ".geojson", ".gpkg", ".pb", ".pb2"]
    if not output_format in supported_formats:
        print(
            f"Error! Format {output_format} not recognized, currently supported formats are: {supported_formats}"
        )
        return None
    if output_format == ".pb" or output_format == ".pb2":
        with open(out_file, "wb") as dst:
            dst.write(city_model.to_proto().SerializeToString())
        return True
    if output_format == ".json":
        protobuf_to_json(city_model, out_file)
        return True
    driver = {
        ".shp": "ESRI Shapefile",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".gpkg": "GPKG",
    }
    crs = city_model.crs
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
        for building in city_model.buildings:
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
