from dtcc_io.cityjson.utils import get_terrain_mesh, get_root_objects, set_buildings
from dtcc_model.object.city import NewCity as City
from dtcc_model.object.object import GeometryType
from dtcc_model.object.terrain import Terrain
from dtcc_model.geometry import Bounds
import numpy as np
from pathlib import Path
import json

def setup_city(cj_obj: dict):
    city = City()
    if "transform" in cj_obj:
        scale = np.array(cj_obj["transform"]["scale"])
        translate = np.array(cj_obj["transform"]["translate"])
    else:
        scale = np.array([1, 1, 1])
        translate = np.array([0, 0, 0])
    if "metadata" in cj_obj:
        if "geographicalExtent" in cj_obj["metadata"]:
            extent = cj_obj["metadata"]["geographicalExtent"]
            city.geometry[GeometryType.BOUNDS] = Bounds(
                extent[0], extent[1], extent[3], extent[4]
            )
    verts = np.array(cj_obj["vertices"]) * scale + translate

    return city, verts


def load(cityjson_path: str) -> City:
    """Load a CityJSON file into a City object."""
    cityjson_path = Path(cityjson_path)
    if not cityjson_path.exists():
        raise FileNotFoundError(f"File {cityjson_path} not found")
    with open(cityjson_path, "r") as f:
        cj = json.load(f)
    if "type" not in cj or cj["type"] != "CityJSON":
        raise ValueError("Not a CityJSON file")
    city, verts = setup_city(cj)
    cj_obj = cj["CityObjects"]

    root_objects = get_root_objects(cj_obj)
    if "Building" in root_objects:
        set_buildings(cj_obj,root_objects["Building"], verts, city)
    if "TINRelief" in root_objects:
        tin = get_terrain_mesh(root_objects["TINRelief"], verts)
        if len(tin.vertices) > 0:
            terrain = Terrain()
            terrain.geometry[GeometryType.MESH] = tin
            city.children[Terrain].append(terrain)
    special_objects = ["Building", "TINRelief"]
    for k, v in root_objects.items():
        if k not in special_objects:
            print(f"Warning: {k} not yet supported")

    return city

