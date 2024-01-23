import copy
import json

import dtcc_model as model
from dataclasses import dataclass, field
import numpy as np


# intermediate stucts used while parsing
@dataclass
class CityBuilding:
    uuid: str
    root: dict
    children: list[dict] = field(default_factory=list)


@dataclass
class CityJSONParts:
    verts: np.ndarray = field(default_factory=lambda: np.empty((0, 3)))
    root_buildings: dict = field(default_factory=dict)
    root_objects: dict = field(default_factory=dict)
    city_objects: dict = field(default_factory=dict)
    bounds: model.geometry.Bounds = field(default_factory=model.geometry.Bounds)


def load_cityjson(path: str) -> model.city:
    """Load a CityJSON file into a CityModel."""
    with open(path, "r") as f:
        cj = json.load(f)
    if "type" not in cj or cj["type"] != "CityJSON":
        raise ValueError("Not a CityJSON file")
    return parse_cityjson(cj)


def parse_cityjson(cj: dict) -> CityJSONParts:
    """Parse a CityJSON file into a CityJSONParts object."""
    cj_obj = CityJSONParts()
    if "transform" in cj:
        scale = np.array(cj["transform"]["scale"])
        translate = np.array(cj["transform"]["translate"])
    else:
        scale = np.array([1, 1, 1])
        translate = np.array([0, 0, 0])
    if "metadata" in cj:
        if "geographicalExtent" in cj["metadata"]:
            extent = cj["metadata"]["geographicalExtent"]
            cj_obj.bounds = model.geometry.Bounds(
                extent[0], extent[1], extent[3], extent[4]
            )
    cj_obj.verts = np.array(cj["vertices"]) * scale + translate
    cj_obj.city_objects.update(cj["CityObjects"])

    for k, v in cj["CityObjects"].items():
        if "parents" not in v:
            if v["type"] == "Building":
                cj_obj.root_buildings[k] = v
            else:
                cj_obj.root_objects[k] = v

    return cj_obj


def parse_buildings(cj_obj):
    buildings = []
    for k, v in cj_obj.root_buildings.items():
        cb = CityBuilding(k, v)
        # print(v)
        for child in v.get("children", []):
            # print(children)
            cb.children.append(cj_obj.city_objects[child])
        buildings.append(cb)
    return buildings

def get_geom_to_use(geom_list, lod=2, prefer_surface=True) -> dict:
    """
Get the geometry we want to use from a list of possible geometries
    Parameters
    ----------
    geom_list: list of possible geometries
    lod: int, prefered level of detail we want, prefer lower to higher if we cannot find exact lod
    prefer_surface: bool, if True, prefer surface to solid

    Returns
    -------
    geom: dict, the geometry we want to use

    """
    if len(geom_list) == 0:
        return {}
    if len(geom_list) == 1:
        return geom_list[0]

    candidates = []
    while len(candidates) == 0:
        for g in geom_list:
            if g["lod"] == lod:
                candidates.append(g)
        lod -= 1
        if lod < 0:
            candidates = geom_list
    if len(candidates) == 1:
        return candidates[0]
    for geom in candidates:
        if "Surface" in geom["type"] and prefer_surface:
            return geom
        elif "Solid" in geom["type"] and not prefer_surface:
            return geom
    return candidates[0]





def get_building_geometry(cj_obj, buildings, lod=2):
    buildings_geom = []
    for b in buildings:
        building_ms = []
        if 'geometry' in b.root:
            building_geometry = b.root['geometry']
            geom = get_geom_to_use(building_geometry, lod=lod)
            ms = build_multisurface(cj_obj, geom)
            ms.properties['semantics'] = geom.get("semantics", {})
            building_ms.append(ms)
        for c in b.root.get("children", []):
            child = cj_obj.city_objects[c]
            geom = child["geometry"]
            geom = get_geom_to_use(geom, lod=lod)
            ms = build_multisurface(cj_obj, geom)
            ms.properties['semantics'] = geom.get("semantics", {})
            building_ms.append(ms)
        buildings_geom.append(building_ms)
    return buildings_geom


def build_multisurface(cj_obj, geom):
    """Build a MultiSurface from a CityJSON geometry."""
    ms = model.geometry.MultiSurface()
    if geom["type"] == "MultiSurface" or geom["type"] == "CompositeSurface":
        boundaries = geom["boundaries"]
    elif geom["type"] == "Solid":
        boundaries = geom["boundaries"][0]
    else:
        raise ValueError(f"Unhandled geometry type {geom['type']}")
    for surface in boundaries:
        s = model.geometry.Surface()
        outer = surface[0]
        inner = surface[1:]
        s.vertices = cj_obj.verts[outer]
        ms.surfaces.append(s)
    return ms
