# Copyright(C) 2023 Anders Logg
# Licensed under the MIT License

from dtcc_model import (
    GridField,
    GridVectorField,
    MeshField,
    MeshVectorField,
    VolumeMeshField,
    VolumeMeshVectorField,
)
from .logging import warning
from . import generic

# FIXME: The proto stuff can be made more generic


def _load_proto_mesh_field(path):
    with open(path, "rb") as f:
        return MeshField.from_proto(f.read())


def _load_proto_mesh_vector_field(path):
    with open(path, "rb") as f:
        return MeshField.from_proto(f.read())


def _save_proto_mesh_field(field, path):
    with open(path, "wb") as f:
        f.write(field.to_proto())


def _save_proto_mesh_vector_field(field, path):
    with open(path, "wb") as f:
        f.write(field.to_proto())


_load_formats = {
    MeshField: {
        ".pb": _load_proto_mesh_field,
        ".pb2": _load_proto_mesh_field,
    },
    MeshVectorField: {
        ".pb": _load_proto_mesh_vector_field,
        ".pb2": _load_proto_mesh_vector_field,
    },
}

_save_formats = {
    MeshField: {
        ".pb": _save_proto_mesh_field,
        ".pb2": _save_proto_mesh_field,
    },
    MeshVectorField: {
        ".pb": _save_proto_mesh_vector_field,
        ".pb2": _save_proto_mesh_vector_field,
    },
}


def load_field(path):
    return generic.load(path, "field", MeshField, _load_formats)


def load_vector_field(path):
    return generic.load(path, "field", MeshVectorField, _load_formats)


def save(mesh, path):
    generic.save(mesh, path, "field", _save_formats)


def list_io():
    return generic.list_io("field", _load_formats, _save_formats)


def print_io():
    generic.print_io("field", _load_formats, _save_formats)
