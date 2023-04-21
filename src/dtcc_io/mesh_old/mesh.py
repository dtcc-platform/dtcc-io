import logging
from pathlib import Path

from dtcc_io.utils import protobuf_to_json, save_to_pb
from dtcc_io.mesh.utils import load_protobuf

from dtcc_io.mesh.meshio_loaders import (
    load_with_meshio,
    save_3d_surface_with_meshio,
    save_3d_volume_mesh_with_meshio,
    save_2d_surface_mesh_with_meshio,
)

try:
    from dtcc_io.mesh.pyassimp_loaders import load_with_assimp

    HAS_ASSIMP = True
except:
    logging.warning(
        "Could not import pyassimp, some file formats will not be supported"
    )
    HAS_ASSIMP = False
from dtcc_io.mesh.pygltflib_loaders import save_3d_surface_with_gltflib
from dtcc_model import Mesh, VolumeMesh

mesh_types = ["surface", "volume", "2d"]


def load_surface3d(path, return_serialized=False):
    path = Path(path)
    suffix = path.suffix.lower()
    reader_libs = {
        ".pb": load_protobuf,
        ".pb2": load_protobuf,
        ".obj": load_with_meshio,
        ".ply": load_with_meshio,
        ".stl": load_with_meshio,
        ".vtk": load_with_meshio,
        ".vtu": load_with_meshio,
    }
    if HAS_ASSIMP:
        reader_libs.update(
            {
                ".dae": load_with_assimp,
                ".fbx": load_with_assimp,
            }
        )

    if suffix in reader_libs:
        pb = reader_libs[suffix](
            path, return_serialized=return_serialized, mesh_type="surface"
        )
    else:
        raise ValueError(f"Unknown file format: {suffix}, must be one of {reader_libs}")
    return pb


def save_surface3d(pb_mesh, path):
    path = str(path)
    writer_libs = {
        "pb": save_to_pb,
        "pb2": save_to_pb,
        "obj": save_3d_surface_with_meshio,
        "ply": save_3d_surface_with_meshio,
        "stl": save_3d_surface_with_meshio,
        "vtk": save_3d_surface_with_meshio,
        "vtu": save_3d_surface_with_meshio,
        "gltf": save_3d_surface_with_gltflib,
        "gltf2": save_3d_surface_with_gltflib,
        "glb": save_3d_surface_with_gltflib,
        "json": protobuf_to_json,
    }
    suffix = path.split(".")[-1].lower()
    if suffix in writer_libs:
        writer_libs[suffix](pb_mesh, path)
    else:
        raise ValueError(
            f"Unknown file format: {suffix}, supported formats are: {list(writer_libs.keys())}"
        )


def load_mesh3d(path, return_serialized=False):
    pass


def save_mesh3d(pb_mesh, path):
    path = str(path)
    writer_libs = {
        "pb": save_to_pb,
        "pb2": save_to_pb,
        "vtk": save_3d_volume_mesh_with_meshio,
        "vtu": save_3d_volume_mesh_with_meshio,
        "json": protobuf_to_json,
    }
    suffix = path.split(".")[-1].lower()
    if suffix in writer_libs:
        writer_libs[suffix](pb_mesh, path)
    else:
        raise ValueError(
            f"Unknown file format: {suffix}, supported formats are: {list(writer_libs.keys())}"
        )


def load_mesh2d(path, return_serialized=False):
    pass


def save_mesh2d(pb_mesh, path):
    path = str(path)
    writer_libs = {
        "pb": save_to_pb,
        "pb2": save_to_pb,
        "vtk": save_2d_surface_mesh_with_meshio,
        "vtu": save_2d_surface_mesh_with_meshio,
        "obj": save_2d_surface_mesh_with_meshio,
        "stl": save_2d_surface_mesh_with_meshio,
        "ply": save_2d_surface_mesh_with_meshio,
        "json": protobuf_to_json,
    }
    suffix = path.split(".")[-1].lower()
    if suffix in writer_libs:
        writer_libs[suffix](pb_mesh, path)
    else:
        raise ValueError(
            f"Unknown file format: {suffix}, supported formats are: {list(writer_libs.keys())}"
        )


def save(pb_mesh, path):
    path = str(path)
    if isinstance(pb_mesh, Mesh):
        save_surface3d(pb_mesh, path)
    if isinstance(pb_mesh, VolumeMesh):
        save_mesh3d(pb_mesh, path)
