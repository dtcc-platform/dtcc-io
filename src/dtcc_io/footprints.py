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
from logging import info, warning, error
from dtcc_model import City, Building, GeometryType, Surface
import numpy as np

from . import generic
from .utils import get_epsg


# from dtcc_model import Polygon, Building, LinearRing, Vector2D, City
import dtcc_model as model
from dtcc_model import Building
from dtcc_model.geometry import Bounds

from .logging import info, warning, error


def building_bounds(shp_footprint_file, buffer=0):
    """
    Calculate the bounding box of a shapefile without loading it.

    Parameters
    ----------
    shp_footprint_file : str
        The path to the shapefile.
    buffer : float, optional
        The buffer distance to add to the bounding box (default 0).

    Returns
    -------
    Bounds
        A `Bounds` object representing the bounding box of the shapefile.
    """
    shp_footprint_file = Path(shp_footprint_file)
    if not shp_footprint_file.is_file():
        raise FileNotFoundError(f"File {shp_footprint_file} not found")
    with fiona.open(shp_footprint_file) as c:
        bbox = Bounds(*c.bounds)
    bbox.buffer(buffer)
    return bbox


def _building_from_fiona(s, uuid_field="id", height_field="", crs=""):
    building = Building()

    if uuid_field in s["properties"]:
        building.id = str(s["properties"][uuid_field])
    if height_field in s["properties"] and s["properties"][height_field]:
        try:
            height = float(s["properties"][height_field])
        except ValueError:
            warning(f"Error cannot parse height field: {s['properties'][height_field]}")
            height = 0.0
    else:
        height = 0.0
    polygon_footprint = shapely.geometry.shape(s["geometry"])
    if not polygon_footprint.is_valid:
        warning(f"Invalid polygon {building.id} attempting to fix...")
        polygon_footprint = polygon_footprint.buffer(0)
        if not polygon_footprint.is_valid:
            error(f"Cannot fix invalid polygon {building.id}")
            return None
    polygon_footprint = shapely.geometry.polygon.orient(polygon_footprint, 1)

    footprint_surface = Surface()

    surface_verts = np.array(polygon_footprint.exterior.coords)
    height = np.zeros(surface_verts.shape[0]) + height
    height = height.reshape(-1, 1)
    surface_verts = np.hstack((surface_verts, height))
    footprint_surface.vertices = surface_verts
    footprint_surface.transform.srs = crs
    building.add_geometry(footprint_surface, GeometryType.LOD0)

    building.attributes.update(s["properties"])
    return building


# def _load_proto_city(filename, *args, **kwargs) -> City:
#     city = City()
#     city.from_proto(filename.read_bytes())
#     return city


def _load_fiona(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds=None,
    min_edge_distance=2.0,
) -> [Building]:
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found")
    buildings = []
    has_height_field = len(height_field) > 0
    bounds_filter = None
    if bounds is not None:
        bounds_filter = shapely.geometry.box(*bounds.tuple).buffer(-min_edge_distance)
    try:
        f = fiona.open(filename)
        f.close()
    except fiona.errors.DriverError:
        raise ValueError(f"File {filename} is not a valid file format")
    with fiona.open(filename) as src:
        info(f"Reading {len(src)} geometries from {filename}")
        crs = get_epsg(src.crs)
        for s in src:
            building_shape = shapely.geometry.shape(s["geometry"])
            if area_filter is not None and area_filter > 0:
                if building_shape.area < area_filter:
                    continue
            if bounds_filter is not None:
                if not bounds_filter.contains(building_shape):
                    continue
            geom_type = s["geometry"]["type"]
            if geom_type == "Polygon":
                building = _building_from_fiona(s, uuid_field, height_field, crs)

                buildings.append(building)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(list(building_shape.geoms)):
                    # make each polygon its own building
                    split_geometry = shapely.geometry.mapping(polygon)
                    split_feature = {
                        "geometry": split_geometry,
                        "properties": s["properties"],
                    }
                    building = _building_from_fiona(
                        split_feature, uuid_field, height_field, crs
                    )

                    buildings.append(building)

    info(f"Loaded {len(buildings)} building footprints")
    return buildings


def load(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds=None,
    min_edge_distance=2.0,
) -> [Building]:
    """
    Load the buildings from a supported file and return a `City` object.

    Parameters
    ----------
    filename : str
        The path to the shapefile.
    uuid_field : str, optional
        The name of the field containing the UUIDs (default "id").
    height_field : str, optional
        The optional name of the field containing the building heights (default "").
    area_filter : float, optional
        The minimum area of a building to include (default None).
    bounds : Bounds, optional
        The bounding box to filter the buildings (default None).
    min_edge_distance : float, optional
        The minimum distance between a building and the bounding box (default 2.0).

    Returns
    -------
    City
        A `City` object representing the city loaded from the shapefile.
    """
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


def _load_proto_city(filename) -> City:
    pass


def _save_proto_city(city: City, filename):
    pass


def _save_json_city(city: City, filename):
    with open(filename, "w") as dst:
        dst.write(city.to_json())


def _save_fiona(city: City, out_file, output_format=""):
    offset = (city.georef.x0, city.georef.y0)
    out_file = Path(out_file)
    output_format = out_file.suffix.lower()
    driver = {
        ".shp": "ESRI Shapefile",
        ".geojson": "GeoJSON",
        ".json": "GeoJSON",
        ".gpkg": "GPKG",
    }
    crs = city.georef.crs.upper()
    if not crs:
        crs = "EPSG:3006"  # current dtcc default
    if driver[output_format] == "GeoJSON" and crs:
        # geojson needs to be in lat/lon
        info(f"Converting from {crs} to EPSG:4326")
        wgs84 = pyproj.CRS("EPSG:4326")
        cm_crs = pyproj.CRS(crs)
        wgs84_projection = pyproj.Transformer.from_crs(cm_crs, wgs84, always_xy=True)
        crs = "EPSG:4326"

    base_properties = {
        "id": "str",
        "height": "float",
        "ground_height": "float",
        "error": "int",
    }
    schema_properties = base_properties.copy()
    for key, value in city.buildings[0].properties.items():
        if key in base_properties:
            continue
        if isinstance(value, int):
            schema_properties[key] = "int"
        elif isinstance(value, float):
            schema_properties[key] = "float"
        elif isinstance(value, str):
            schema_properties[key] = "str"
        elif isinstance(value, bool):
            schema_properties[key] = "bool"
        elif isinstance(value, list):
            info(f"Converting list {key} to string")
            schema_properties[key] = "str"
        else:
            schema_properties[key] = "str"
            warning(f"Cannot determine type of attribute {key}, assuming 'str'")

    schema = {"geometry": "Polygon", "properties": schema_properties}
    with fiona.open(
        out_file, "w", driver=driver[output_format], schema=schema, crs=crs
    ) as dst:
        for building in city.buildings:
            shapely_footprint = building.footprint
            shapely_footprint = shapely.affinity.translate(
                shapely_footprint, xoff=offset[0], yoff=offset[1]
            )
            if driver[output_format] == "GeoJSON":
                shapely_footprint = shapely.ops.transform(
                    wgs84_projection.transform, shapely_footprint
                )
            properties = {
                "id": building.uuid,
                "height": building.height,
                "ground_height": building.ground_level,
                "error": building.error,
            }
            for key in schema_properties.keys():
                if key in base_properties:
                    continue
                if key in building.properties:
                    v = building.properties[key]
                    if isinstance(v, list):
                        v = ",".join([str(v) for v in v])
                    properties[key] = v
                else:
                    properties[key] = None

            dst.write(
                {
                    "geometry": shapely.geometry.mapping(shapely_footprint),
                    "properties": properties,
                }
            )


def save(city, filename):
    """
    Save the buildings in a `City` object to a supported file.

    Parameters
    ----------
    city : City
        A `City` object.
    filename : str or path
        The path to the output file.
    """
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
