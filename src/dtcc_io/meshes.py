# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

from dtcc_model import Mesh, VolumeMesh
from .logging import info, error


def load(path):
    pass


def save(mesh, path):
    path = str(path)
    if isinstance(mesh, Mesh):
        save_mesh(mesh, path)
    elif isinstance(mesh, VolumeMesh):
        save_volume_mesh(mesh, path)
    else:
        error('Unable to save mesh of type "%s"' % type(mesh))


def save_mesh(mesh, path):
    info(f"Saving DTCC Mesh to {path}")


def save_volume_mesh(mesh, path):
    info(f"Saving DTCC VolumeMesh to {path}")
