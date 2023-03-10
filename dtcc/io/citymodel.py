# Copyright (C) 2022 Dag Wästberg
# Licensed under the MIT License

#%%
import json

import shapely.geometry
import fiona



from dtcc.io.dtcc_model.protobuf.dtcc_pb2 import (
    Polygon,
    Building,
    LinearRing,
    Vector2D,
    CityModel,
)

def building_bounds(shp_footprint_file, buffer=0):
    """calculate the bounding box of a shp file without loading it"""
    with fiona.open(shp_footprint_file) as c:
        bbox = c.bounds
    if buffer != 0:
        px, py, qx, qy = bbox
        bbox = (px - buffer, py - buffer, qx + buffer, qy + buffer)
    return bbox

#%%
def cleanLinearRing(coords, tol=0.1):
    # s = shapely.geometry.Polygon(coords)
    # s = shapely.geometry.Polygon.orient(s, 1)  # make ccw
    # s = s.simplify(tol)
    # return list(s.exterior.coords)[:-1]
    return coords


#%%
def buildLinearRing(coords, clean=True):
    if clean:
        coords = cleanLinearRing(coords)
    lr = LinearRing()
    vertices = []
    for c in coords:
        v = Vector2D()
        v.x = c[0]
        v.y = c[1]
        vertices.append(v)
    lr.vertices.extend(vertices)
    return lr


def buildPolygon(geom_coords, clean=True):
    polygon = Polygon()
    shell = geom_coords.pop(0)
    shell = buildLinearRing(shell, clean)
    polygon.shell.CopyFrom(shell)
    if len(geom_coords) > 0:
        holes = []
        for hole in geom_coords:
            hole = buildLinearRing(hole, clean)
            holes.append(hole)
        polygon.holes.extend(holes)
    return polygon


def pbFootprint2Shapely(pb_footprint):
    shell = []
    holes = []
    for vert in pb_footprint.shell.vertices:
        shell.append((vert.x, vert.y))
    for h in pb_footprint.holes:
        hole = []
        for vert in h.vertices:
            hole.append((vert.x, vert.y))
        if len(hole) > 0:
            holes.append(hole)
    poly = shapely.geometry.Polygon(shell, holes=holes)
    return poly


def read(
    filename,
    uuid_field="id",
    height_field="",
    area_filter=None,
    bounds = None,
    min_edge_distance = 2.0,
    return_serialized=False,
):
    cityModel = CityModel()
    buildings = []
    has_height_field = len(height_field) > 0
    if bounds is not None:
        bounds = shapely.geometry.box(*bounds).buffer(-min_edge_distance)
    with fiona.open(filename) as src:
        for s in src:

            if area_filter is not None and area_filter > 0:

                if shapely.geometry.shape(s["geometry"]).area < area_filter:
                    continue
            if bounds is not None:
                if not shapely.geometry.shape(s["geometry"]).intersects(bounds):
                    continue
            geom_type = s["geometry"]["type"]
            if geom_type == "Polygon":
                building = Building()
                if uuid_field in s["properties"]:
                    building.uuid = str(s["properties"][uuid_field])
                if (
                    has_height_field
                    and height_field in s["properties"]
                    and s["properties"][height_field]
                ):
                    try:
                        building.height = float(s["properties"][height_field])
                    except ValueError:
                        print(
                            f"Error cannot parse height field: {s['properties'][height_field]}"
                        )

                footprint = buildPolygon(s["geometry"]["coordinates"])
                building.footPrint.CopyFrom(footprint)
                buildings.append(building)
            if geom_type == "MultiPolygon":
                for idx, polygon in enumerate(s["geometry"]["coordinates"]):
                    building = Building()
                    if uuid_field in s["properties"]:
                        uuid = str(s["properties"][uuid_field]) + f"-{idx}"
                        building.uuid = uuid
                    if (
                        has_height_field
                        and height_field in s["properties"]
                        and s["properties"][height_field]
                    ):
                        try:
                            building.height = float(s["properties"][height_field])
                        except ValueError:
                            print(
                                f"Error cannot parse height field: {s['properties'][height_field]}"
                            )
                    footprint = buildPolygon(polygon)
                    building.footPrint.CopyFrom(footprint)
                    buildings.append(building)
    cityModel.buildings.extend(buildings)
    if return_serialized:
        return cityModel.SerializeToString()
    else:
        return cityModel


def loadCityModelJson(
    citymodel_path,
    return_serialized=False,
):
    with open(citymodel_path) as src:
        citymodelJson = json.load(src)
    cityModel = CityModel()
    buildings = []
    for b in citymodelJson["Buildings"]:
        building = Building()
        if isinstance(b["Footprint"], list):
            shell = [(v["x"], v["y"]) for v in b["Footprint"]]
            holes = []
        else:
            shell = [(v["x"], v["y"]) for v in b["Footprint"]["shell"]]
            holes = []
            for hole in b["Footprint"]["holes"]:
                h = [(v["x"], v["y"]) for v in hole]
                holes.append(h)
        footprint = buildPolygon([shell, holes], clean=False)
        building.footPrint.CopyFrom(footprint)
        building.height = b["Height"]
        building.groundHeight = b["GroundHeight"]
        building.uuid = b["UUID"]
        building.error = b["Error"]
        buildings.append(building)
    cityModel.buildings.extend(buildings)
    if return_serialized:
        return cityModel.SerializeToString()
    else:
        return cityModel


def write(city_model, out_file, output_format=""):
    if output_format == "":
        output_format = out_file.split(".")[-1].lower()
    if not output_format.startswith("."):
        output_format = "." + output_format
    if not output_format in [".shp", ".json", ".geojson", ".gpkg"]:
        print(f"Error! Format {output_format} not recognized")
        return None
    driver = {
        ".shp": "ESRI Shapefile",
        ".json": "GeoJSON",
        ".geojson": "GeoJSON",
        ".gpkg": "GPKG",
    }

    schema = {
        "geometry": "Polygon",
        "properties": {"id": "str", "height": "float", "ground_height": "float"},
    }
    with fiona.open(out_file, "w", driver[output_format], schema) as dst:
        for building in city_model.buildings:
            shapely_footprint = pbFootprint2Shapely(building.footPrint)
            dst.write(
                {
                    "geometry": shapely.geometry.mapping(shapely_footprint),
                    "properties": {
                        "id": building.uuid,
                        "height": building.height,
                        "ground_height": building.groundHeight,
                    },
                }
            )
