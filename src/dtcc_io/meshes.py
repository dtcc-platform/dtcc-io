# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

import meshio
import pathlib

from dtcc_model import Mesh, VolumeMesh
from .logging import info, error


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


_load_mesh_format = {
    ".pb": _load_mesh_proto,
    ".pb2": _load_mesh_proto,
    ".obj": _load_mesh_meshio,
    ".ply": _load_mesh_meshio,
    ".stl": _load_mesh_meshio,
    ".vtk": _load_mesh_meshio,
    ".vtu": _load_mesh_meshio,
}

_load_volume_mesh_format = {}

_save_mesh_format = {
    ".pb": _save_mesh_proto,
    ".pb2": _save_mesh_proto,
    ".obj": _save_mesh_meshio,
    ".ply": _save_mesh_meshio,
    ".stl": _save_mesh_meshio,
    ".vtk": _save_mesh_meshio,
    ".vtu": _save_mesh_meshio,
}

_save_volume_mesh_format = {}


def _load_mesh(mesh, path):
    info(f"Loading Mesh from {path}")
    if path.suffix in _load_mesh_format:
        _load_mesh_format[path.suffix](mesh, path)
    else:
        error(f'Unable to load Mesh; format "{path.suffix}" not supported')


def _load_volume_mesh(mesh, path):
    info(f"Loading VolumeMesh from {path}")
    if path.suffix in _load_volume_mesh_format:
        _load_volume_mesh_format[path.suffix](mesh, path)
    else:
        error(f'Unable to load VolumeMesh; format "{path.suffix}" not supported')


def _save_mesh(mesh, path):
    info(f"Saving Mesh to {path}")
    if path.suffix in _save_mesh_format:
        _save_mesh_format[path.suffix](mesh, path)
    else:
        error(f'Unable to save Mesh; format "{path.suffix}" not supported')


def _save_volume_mesh(mesh, path):
    info(f"Saving VolumeMesh to {path}")
    if path.suffix in _save_volume_mesh_format:
        _save_volume_mesh_format[path.suffix](mesh, path)
    else:
        error(f'Unable to save VolumeMesh; format "{path.suffix}" not supported')


_load_mesh_type = {
    Mesh: _load_mesh,
    VolumeMesh: _load_volume_mesh,
}


_save_mesh_type = {
    Mesh: _save_mesh,
    VolumeMesh: _save_volume_mesh,
}


def load(mesh, path):
    if type(mesh) in _load_mesh_type:
        path = pathlib.Path(path)
        _load_mesh_type[type(mesh)](mesh, path)
    else:
        error(f'Unable to load mesh; type "{type(mesh)}" not supported' % type(mesh))


def save(mesh, path):
    if type(mesh) in _save_mesh_type:
        path = pathlib.Path(path)
        _save_mesh_type[type(mesh)](mesh, path)
    else:
        error(f'Unable to save mesh; type "{type(mesh)}" not supported' % type(mesh))
