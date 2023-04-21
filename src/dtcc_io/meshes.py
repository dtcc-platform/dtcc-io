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


def _load_proto_mesh(path):
    with open(path, "rb") as f:
        return Mesh.from_proto(f.read())


def _load_proto_volume_mesh(path):
    with open(path, "rb") as f:
        return VolumeMesh.from_proto(f.read())


def _save_proto_mesh(mesh, path):
    with open(path, "wb") as f:
        f.write(mesh.to_proto())


def _save_proto_volume_mesh(volume_mesh, path):
    with open(path, "wb") as f:
        f.write(volume_mesh.to_proto())


def _load_meshio_mesh(path):
    mesh = meshio.read(path)
    vertices = mesh.points
    faces = mesh.cells[0].data
    return Mesh(vertices=vertices, faces=faces)


def _load_meshio_volume_meshio(path):
    pass


def _save_meshio_mesh(mesh, path):
    _mesh = meshio.Mesh(mesh.vertices, [("triangle", mesh.faces)])
    meshio.write(path, _mesh)


def _save_mesh_gltflib(mesh, path):
    pass


_load_formats = {
    Mesh: {
        ".pb": _load_proto_mesh,
        ".pb2": _load_proto_mesh,
        ".obj": _load_meshio_mesh,
        ".ply": _load_meshio_mesh,
        ".stl": _load_meshio_mesh,
        ".vtk": _load_meshio_mesh,
        ".vtu": _load_meshio_mesh,
    },
    VolumeMesh: {
        ".pb": _load_proto_volume_mesh,
        ".pb2": _load_proto_volume_mesh,
    },
}

_save_formats = {
    Mesh: {
        ".pb": _save_proto_mesh,
        ".pb2": _save_proto_mesh,
        ".obj": _save_meshio_mesh,
        ".ply": _save_meshio_mesh,
        ".stl": _save_meshio_mesh,
        ".vtk": _save_meshio_mesh,
        ".vtu": _save_meshio_mesh,
        ".gltf": _save_mesh_gltflib,
        ".gltf2": _save_mesh_gltflib,
        ".glb": _save_mesh_gltflib,
    },
    VolumeMesh: {
        ".pb": _save_proto_volume_mesh,
        ".pb2": _save_proto_volume_mesh,
    },
}

if HAS_ASSIMP:
    _load_formats[Mesh].update(
        {
            ".dae": load_assimp_mesh,
            ".fbx": load_assimp_mesh,
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
