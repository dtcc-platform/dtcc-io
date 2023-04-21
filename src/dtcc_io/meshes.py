# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

import meshio
import pathlib

from dtcc_model import Mesh, VolumeMesh
from . import generic


def _load_mesh_proto(path):
    pass


def _load_mesh_meshio(path):
    pass


def _load_volume_mesh_proto(path):
    pass


def _load_volume_mesh_meshio(path):
    pass


def _save_mesh_proto(mesh, path):
    pass


def _save_mesh_meshio(mesh, path):
    pass


def _save_volume_mesh_proto(mesh, path):
    pass


def _save_volume_mesh_meshio(mesh, path):
    pass


save_to_pb = lambda object, path: None
save_3d_surface_with_meshio = lambda object, path: None
save_3d_surface_with_gltflib = lambda object, path: None
protobuf_to_json = None

_load_formats = {
    Mesh: {
        ".pb": _load_mesh_proto,
        ".pb2": _load_mesh_proto,
        ".obj": _load_mesh_meshio,
        ".ply": _load_mesh_meshio,
        ".stl": _load_mesh_meshio,
        ".vtk": _load_mesh_meshio,
        ".vtu": _load_mesh_meshio,
    },
    VolumeMesh: {},
}

_save_formats = {
    Mesh: {
        ".pb": save_to_pb,
        ".pb2": save_to_pb,
        ".obj": save_3d_surface_with_meshio,
        ".ply": save_3d_surface_with_meshio,
        ".stl": save_3d_surface_with_meshio,
        ".vtk": save_3d_surface_with_meshio,
        ".vtu": save_3d_surface_with_meshio,
        ".gltf": save_3d_surface_with_gltflib,
        ".gltf2": save_3d_surface_with_gltflib,
        ".glb": save_3d_surface_with_gltflib,
        ".json": protobuf_to_json,
    },
    VolumeMesh: {},
}


def load_mesh(path):
    generic.load(path, "mesh", _load_formats[Mesh])


def load_volume_mesh(path):
    generic.load(path, "volume mesh", VolumeMesh, _load_formats)


def save(mesh, path):
    generic.save(mesh, path, "mesh", _save_formats)


def list_io():
    return generic.list_io("mesh", _load_formats, _save_formats)


def print_io():
    generic.print_io("mesh", _load_formats, _save_formats)
