import pygltflib
from pathlib import Path
import numpy as np
from dtcc_model import Mesh
import base64


def save_3d_surface_with_gltflib(pb_mesh, path):
    suffix = Path(path).suffix.lower()
    if suffix.startswith(".gltf"):
        write_format = "json"
    elif suffix.startswith(".glb"):
        write_format = "binary"
    if type(pb_mesh) == bytes:
        surface = Mesh()
        surface.ParseFromString(pb_mesh)
    else:
        surface = pb_mesh
    vertices = np.array([[v.x, v.y, v.z] for v in surface.vertices], dtype=np.float32)
    faces = np.array([[f.v0, f.v1, f.v2] for f in surface.faces], dtype=np.uint32)
    # normals = [[n.x, n.y, n.z] for n in surface.normals]
    # data = np.concatenate([vertices, faces]).tobytes()

    triangles_binary_blob = faces.flatten().tobytes()
    points_binary_blob = vertices.tobytes()
    data = triangles_binary_blob + points_binary_blob

    # Create a glTF asset
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
        count=faces.size,
        type=pygltflib.SCALAR,
        max=[int(faces.max())],
        min=[int(faces.min())],
    )
    model.accessors.append(triangle_accessor)
    points_accessor = pygltflib.Accessor(
        bufferView=1,
        componentType=pygltflib.FLOAT,
        count=len(vertices),
        type=pygltflib.VEC3,
        max=vertices.max(axis=0).tolist(),
        min=vertices.min(axis=0).tolist(),
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

    if write_format == "json":
        buffer.uri = "data:application/octet-stream;base64," + base64.b64encode(
            data
        ).decode("utf-8")
    elif write_format == "binary":
        model.set_binary_blob(data)

    model.save(path)
    return True
