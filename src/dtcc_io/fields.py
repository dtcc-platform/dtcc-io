# Copyright(C) 2023 Anders Logg
# Licensed under the MIT License

from dtcc_model import (
    MeshField,
    MeshVectorField,
    VolumeMeshField,
    VolumeMeshVectorField,
)

from .logging import info, error


def load(path):
    pass


def save(field, path):
    if isinstance(field, MeshField):
        save_mesh_field(field, path)
    elif isinstance(field, MeshVectorField):
        save_mesh_vector_field(field, path)
    elif isinstance(field, VolumeMeshField):
        save_volume_mesh_field(field, path)
    elif isinstance(field, VolumeMeshVectorField):
        save_volume_mesh_vector_field(field, path)
    else:
        error('Unable to save field of type "%s"' % type(field))


def save_mesh_field(field, path):
    info(f"Saving MeshField to {path}")


def save_mesh_vector_field(field, path):
    info(f"Saving MeshVectorField to {path}")


def save_volume_mesh_field(field, path):
    info(f"Saving VolumeMeshField to {path}")


def save_volume_mesh_vector_field(field, path):
    info(f"Saving VolumeMeshVectorField to {path}")
