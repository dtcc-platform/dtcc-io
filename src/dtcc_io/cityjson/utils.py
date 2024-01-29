import numpy as np

from dtcc_model import Mesh, MultiSurface, Surface, NewBuilding as Building, NewCity as City
from dtcc_model.object.building import BuildingPart
from dtcc_model.object.object import GeometryType


def tin_geom_to_mesh(tin_geom, verts) -> Mesh:
    mesh = Mesh()
    faces = []
    for geom in tin_geom["geometry"]:
        vert_dict = {}
        faces += [face[0] for face in geom["boundaries"]]
        for face in faces:
            vert_dict[face[0]] = verts[face[0]]
            vert_dict[face[1]] = verts[face[1]]
            vert_dict[face[2]] = verts[face[2]]

    fv_map = [(f, v) for f, v in vert_dict.items()]
    fv_map.sort(key=lambda x: x[0])
    vert_map = {f: i for i, f in enumerate([f for f, v in fv_map])}
    mesh.vertices = np.array([v for f, v in fv_map])
    mesh.faces = np.array([[vert_map[f] for f in face] for face in faces])
    return mesh


def get_terrain_mesh(cj_obj: dict, verts: np.ndarray) -> Mesh:
    tin_geom = []
    for geom in cj_obj.values():
        if geom['type'] == 'TINRelief':
            tin_geom.append(tin_geom_to_mesh(geom, verts))
    if len(tin_geom) == 0:
        return Mesh()
    if len(tin_geom) == 1:
        return tin_geom[0]
    else:
        #TODO: implement mesh merging i wrangler
        # return tin_geom[0].merge(tin_geom[1:])
        return tin_geom[0]


def build_multisurface(geom, verts):
    """Build a MultiSurface from a CityJSON geometry."""
    ms = MultiSurface()
    if not isinstance(geom, dict):
        pass
    if geom["type"] == "MultiSurface" or geom["type"] == "CompositeSurface":
        boundaries = geom["boundaries"]
    elif geom["type"] == "Solid":
        boundaries = geom["boundaries"][0]
    else:
        raise ValueError(f"Unhandled geometry type {geom['type']}")
    for surface in boundaries:
        s = Surface()
        outer = surface[0]
        inner = surface[1:]
        s.vertices = verts[outer]
        ms.surfaces.append(s)
    return ms


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


def get_building_geometry(cj_obj,building, verts, lod=2):
    building_root_geom = None
    building_children = []
    if 'geometry' in building:
        building_geometry = building['geometry']
        geom = get_geom_to_use(building_geometry, lod=lod)
        ms = build_multisurface(geom, verts)
        #ms.properties['semantics'] = geom.get("semantics", {})
        building_root_geom = (geom,ms)
    for c in building.get("children", []):
        child = cj_obj[c]
        geom = child["geometry"]
        geom = get_geom_to_use(geom, lod=lod)
        ms = build_multisurface(geom,verts)
        building_children.append((geom,ms))
    return building_root_geom, building_children


def build_dtcc_building(cj_obj,uuid, cj_building, verts, parent_city, lod=2):
    building = Building()
    building.parents[City] = [parent_city]
    parent_city.children[Building].append(building)
    building.id = uuid
    building.attributes = cj_building.get('attributes',{})
    building_root_geom, building_children = get_building_geometry(cj_obj, cj_building, verts, lod=lod)
    if building_root_geom is not None:
        geom, ms = building_root_geom
        lod = geom.get('lod', 1)
        lod = GeometryType.from_str(f"lod{lod}")
        building.geometry[lod] = ms
    for geom, ms in building_children:
        lod = geom.get('lod', 1)
        building_part = BuildingPart()
        building_part.parents[Building] = [building]
        building.children[BuildingPart].append(building_part)
        lod = GeometryType.from_str(f"lod{lod}")
        building_part.geometry[lod] = ms


def get_root_buildings(cj_obj: dict):
    cj_root_buildings = []
    for k,v in cj_obj.items():
        if "parents" not in v:
            if v["type"] == "Building":
                cj_root_buildings.append((k,v))
    return cj_root_buildings


def get_buildings(cj_obj: dict, verts: np.ndarray, parent_city: City, lod=2) -> [Building]:
    root_buildings = get_root_buildings(cj_obj)
    buildings = []
    for uuid,v in root_buildings:
        buildings.append(build_dtcc_building(cj_obj,uuid,v, verts, parent_city, lod=lod))
