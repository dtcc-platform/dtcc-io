# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

import meshio
import pathlib

from dtcc_model import Mesh, VolumeMesh
from .logging import warning
from . import generic

try:
    import pyassimp

    HAS_ASSIMP = True
except:
    warning("Unable to pyassimp, some file formats will not be supported")
    HAS_ASSIMP = False


def _load_mesh_proto(path):
    with open(path, "rb") as f:
        return Mesh.from_proto(f.read())


def _load_mesh_meshio(path):
    mesh = meshio.read(path)
    vertices = mesh.points
    faces = mesh.cells[0].data
    return Mesh(vertices=vertices, faces=faces)


def _save_mesh_proto(mesh, path):
    with open(path, "wb") as f:
        f.write(mesh.to_proto())


def _save_mesh_meshio(mesh, path):
    _mesh = meshio.Mesh(mesh.vertices, [("triangle", mesh.faces)])
    meshio.write(path, _mesh)


def _save_mesh_gltflib(mesh, path):
    pass


def _load_volume_mesh_proto(path):
    with open(path, "rb") as f:
        return VolumeMesh.from_proto(f.read())


def _save_volume_mesh_proto(volume_mesh, path):
    with open(path, "wb") as f:
        f.write(volume_mesh.to_proto())


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
    VolumeMesh: {
        ".pb": _load_volume_mesh_proto,
        ".pb2": _load_volume_mesh_proto,
    },
}

_save_formats = {
    Mesh: {
        ".pb": _save_mesh_proto,
        ".pb2": _save_mesh_proto,
        ".obj": _save_mesh_meshio,
        ".ply": _save_mesh_meshio,
        ".stl": _save_mesh_meshio,
        ".vtk": _save_mesh_meshio,
        ".vtu": _save_mesh_meshio,
        ".gltf": _save_mesh_gltflib,
        ".gltf2": _save_mesh_gltflib,
        ".glb": _save_mesh_gltflib,
    },
    VolumeMesh: {
        ".pb": _save_volume_mesh_proto,
        ".pb2": _save_volume_mesh_proto,
    },
}

if HAS_ASSIMP:
    _load_formats[Mesh].update(
        {
            ".dae": load_with_assimp,
            ".fbx": load_with_assimp,
        }
    )


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
