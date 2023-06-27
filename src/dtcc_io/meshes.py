# Copyright(C) 2023 Anders Logg and Dag Wästberg
# Licensed under the MIT License

import meshio
import pygltflib
import numpy as np

from dtcc_model import Mesh, VolumeMesh
from dtcc_common import warning, error, info
from . import generic

try:
    import pyassimp

    HAS_ASSIMP = True
except:
    warning("Unable to find pyassimp, some file formats will not be supported")
    HAS_ASSIMP = False


def _load_proto_mesh(path):
    with open(path, "rb") as f:
        return Mesh.from_proto(f.read())


def _load_proto_volume_mesh(path):
    with open(path, "rb") as f:
        return VolumeMesh.from_proto(f.read())


def _save_proto_mesh(mesh, path):
    with open(path, "wb") as f:
        f.write(mesh.to_proto().SerializeToString())


def _save_proto_volume_mesh(mesh, path):
    with open(path, "wb") as f:
        f.write(mesh.to_proto().SerializeToString())


def _load_meshio_mesh(path):
    mesh = meshio.read(path)
    vertices = mesh.points[:, :3]
    vertex_colors = np.empty(0)
    if mesh.points.shape[1] > 3:
        vertex_colors = mesh.points[:, 3:]
    faces = mesh.cells[0].data
    # FIXME: What about normals?
    return Mesh(vertices=vertices, vertex_colors=vertex_colors, faces=faces)


def _load_meshio_volume_mesh(path):
    mesh = meshio.read(path)
    vertices = mesh.points[:, :3]
    cells = mesh.cells[0].data
    return VolumeMesh(vertices=vertices, cells=cells)


def _save_meshio_mesh(mesh, path):
    print(mesh.vertices.shape, mesh.faces.shape)
    _mesh = meshio.Mesh(mesh.vertices, [("triangle", mesh.faces)])
    meshio.write(path, _mesh)


def _save_meshio_volume_mesh(mesh, path):
    _mesh = meshio.Mesh(mesh.vertices, [("tetra", mesh.cells)])
    meshio.write(path, _mesh)


def _save_gltf_mesh(mesh, path):
    triangles_binary_blob = mesh.faces.flatten().tobytes()
    points_binary_blob = mesh.vertices.flatten().tobytes()
    data = triangles_binary_blob + points_binary_blob

    model = pygltflib.GLTF2()
    scene = pygltflib.Scene(nodes=[0])
    model.scenes.append(scene)
    model.scene = 0
    nodes = pygltflib.Node(mesh=0)
    model.nodes.append(nodes)

    buffer = pygltflib.Buffer()
    buffer.byteLength = len(data)
    model.buffers.append(buffer)
    model.set_binary_blob(data)

    triangle_accessor = pygltflib.Accessor(
        bufferView=0,
        componentType=pygltflib.UNSIGNED_INT,
        count=mesh.faces.size,
        type=pygltflib.SCALAR,
        max=[int(mesh.faces.max())],
        min=[int(mesh.faces.min())],
    )
    model.accessors.append(triangle_accessor)
    points_accessor = pygltflib.Accessor(
        bufferView=1,
        componentType=pygltflib.FLOAT,
        count=len(mesh.vertices),
        type=pygltflib.VEC3,
        max=mesh.vertices.max(axis=0).tolist(),
        min=mesh.vertices.min(axis=0).tolist(),
    )
    model.accessors.append(points_accessor)

    triangle_view = pygltflib.BufferView(
        buffer=0,
        byteLength=len(triangles_binary_blob),
        byteOffset=0,
        target=pygltflib.ELEMENT_ARRAY_BUFFER,
    )
    model.bufferViews.append(triangle_view)
    points_view = pygltflib.BufferView(
        buffer=0,
        byteLength=len(points_binary_blob),
        byteOffset=len(triangles_binary_blob),
        target=pygltflib.ARRAY_BUFFER,
    )
    model.bufferViews.append(points_view)

    mesh = pygltflib.Mesh()
    primitive = pygltflib.Primitive(attributes={"POSITION": 1}, indices=0)
    mesh.primitives.append(primitive)
    model.meshes.append(mesh)

    # FIXME: Figure out how to handle optional arguments
    # if write_format == "json":
    #    buffer.uri = "data:application/octet-stream;base64," + base64.b64encode(
    #        data
    #    ).decode("utf-8")
    # elif write_format == "binary":
    #    model.set_binary_blob(data)

    model.set_binary_blob(data)
    model.save(path)


def _load_assimp_mesh(path):
    scene = pyassimp.load(str(path), pyassimp.postprocess.aiProcess_Triangulate)
    _mesh = scene.meshes[0]
    return Mesh(vertices=_mesh.vertices, normals=_mesh.normals, faces=_mesh.faces)


def _save_assimp_mesh(mesh, path):
    error("Not implemented, please FIXME")


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
        ".obj": _load_meshio_mesh,
        ".ply": _load_meshio_mesh,
        ".stl": _load_meshio_mesh,
        ".vtk": _load_meshio_mesh,
        ".vtu": _load_meshio_mesh,
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
        ".gltf": _save_gltf_mesh,
        ".gltf2": _save_gltf_mesh,
        ".glb": _save_gltf_mesh,
    },
    VolumeMesh: {
        ".pb": _save_proto_volume_mesh,
        ".pb2": _save_proto_volume_mesh,
        ".obj": _save_meshio_volume_mesh,
        ".ply": _save_meshio_volume_mesh,
        ".stl": _save_meshio_volume_mesh,
        ".vtk": _save_meshio_volume_mesh,
        ".vtu": _save_meshio_volume_mesh,
    },
}

if HAS_ASSIMP:
    _load_formats[Mesh].update(
        {
            ".dae": _load_assimp_mesh,
            ".fbx": _load_assimp_mesh,
        }
    )
    _save_formats[Mesh].update(
        {
            ".dae": _save_assimp_mesh,
            ".fbx": _save_assimp_mesh,
        }
    )


def load_mesh(path):
    info("Loading mesh from %s" % path)
    return generic.load(path, "mesh", Mesh, _load_formats)


def load_volume_mesh(path):
    info("Loading volume mesh from %s" % path)
    return generic.load(path, "mesh", VolumeMesh, _load_formats)


def save(mesh, path):
    info("Saving mesh to %s" % path)
    generic.save(mesh, path, "mesh", _save_formats)


def list_io():
    return generic.list_io("mesh", _load_formats, _save_formats)


def print_io():
    generic.print_io("mesh", _load_formats, _save_formats)
