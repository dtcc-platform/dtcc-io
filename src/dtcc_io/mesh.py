import pyassimp
import pyassimp.postprocess
import meshio
import numpy as np
from pathlib import Path

from .utils import protobuf_to_json
from dtcc_model import Vector3D, Simplex2D, Surface3D, Mesh3D, Mesh2D

mesh_types = ["surface", "volume", "2d"]

def load(path, return_serialized=False, mesh_type="surface"):
    
    
    mesh_type = mesh_type.lower()

    if mesh_type not in mesh_types:
        raise ValueError(f"Unknown mesh type: {mesh_type}, must be one of {mesh_types}")
    path = Path(path)
    suffix = path.suffix.lower()[1:] # remove leading dot
    reader_libs = {
        "pb":   load_protobuf,
        "pb2":  load_protobuf,
        "obj": load_with_meshio,
        "ply": load_with_meshio,
        "stl": load_with_meshio,
        "vtk": load_with_meshio,
        "vtu": load_with_meshio,

        "dae": load_with_assimp,
        "fbx": load_with_assimp,
        "gltf": load_with_assimp,
        "glb": load_with_assimp
    }
    print(f"Reading mesh from {path}")
    if suffix in reader_libs:
        pb = reader_libs[suffix](path, return_serialized=return_serialized, mesh_type = mesh_type)
    else:
        raise ValueError(f"Unknown file format: {suffix}")
    return pb
    # mesh = meshio.read(path)
    # print(mesh)
    # scene = pyassimp.load(path) #, pyassimp.postprocess.aiProcess_Triangulate)
    # print(f"Loaded {len(scene.meshes)} meshes")
    # mesh = scene.meshes[0]
    # if mesh.vertices.shape[1] == 3:
    #     if mesh.faces.shape[1] == 3:
    #         return load_3d_surface(mesh, return_serialized)
    #     else:
    #         raise NotImplementedError(
    #             "Only triangular surface meshes are supported"
    #         )
    # else:
    #     print(f"Cannot read mesh with {mesh.vertices.shape[1]} dimensions")

def load_protobuf(path, return_serialized=False, mesh_type="surface"):
    if return_serialized:
        return open(path, "rb").read()
    if mesh_type == "surface":
        pb_mesh = Surface3D()
    elif mesh_type == "volume":
        pb_mesh = Mesh3D()
    elif mesh_type == "2d":
        pb_mesh = Mesh2D()
    else:
        raise ValueError(f"Unknown mesh type: {mesh_type}, must be one of {mesh_types}")
    with open(path, "rb") as f:
        pb_mesh.ParseFromString(f.read())
    return pb_mesh

def load_with_assimp(path, return_serialized=False, mesh_type="surface"):
    scene = pyassimp.load(path, pyassimp.postprocess.aiProcess_Triangulate)
    print(f"Loaded {len(scene.meshes)} meshes")
    mesh = scene.meshes[0]
    print(mesh)
    print(mesh.vertices.shape)
    print(mesh.faces.shape)
    return create_3d_surface(mesh.vertices, mesh.faces, mesh.normals, return_serialized=return_serialized)


def load_with_meshio(path, return_serialized=False, mesh_type="surface"):
    mesh = meshio.read(path)
    # print(mesh)
    vertices = mesh.points
    faces = mesh.cells[0].data
    return create_3d_surface(vertices, faces, return_serialized=return_serialized)


def create_3d_surface(vertices, faces, normals=None, return_serialized=False):
    pb = Surface3D()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=v[2]) for v in vertices])
    pb.faces.extend([Simplex2D(v0=f[0], v1=f[1], v2=f[2]) for f in faces])
    if normals is not None:
        pb.normals.extend([Vector3D(x=n[0], y=n[1], z=n[2]) for n in normals])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb


def save(pb_mesh, path):
    path = str(path)
    if isinstance(pb_mesh, Surface3D):
        writer_libs = {
            "pb": save_to_pb,
            "pb2": save_to_pb,
            "obj": save_3d_surface_with_meshio,
            "ply": save_3d_surface_with_meshio,
            "stl": save_3d_surface_with_meshio,
            "vtk": save_3d_surface_with_meshio,
            "vtu": save_3d_surface_with_meshio,
            "json" : protobuf_to_json
        }
    if isinstance(pb_mesh, Mesh3D):
        writer_libs = {
            "pb": save_to_pb,
            "pb2": save_to_pb,
            "vtk": save_3d_volume_mesh_with_meshio,
            "vtu": save_3d_volume_mesh_with_meshio,
            "json" : protobuf_to_json
        }
    if isinstance(pb_mesh, Mesh2D):
        raise NotImplementedError("Writing 2D meshes is not implemeted yet")
    suffix = path.split(".")[-1].lower()
    if suffix in writer_libs:
        writer_libs[suffix](path, pb_mesh)
    else:
        raise ValueError(
            f"Unknown file format: {suffix}, supported formats are: {list(writer_libs.keys())}")
    
def save_to_pb(path, pb_mesh):
    with open(path, "wb") as f:
        f.write(pb_mesh.SerializeToString())

def save_3d_surface_with_meshio(path, pb_surface):
    if type(pb_surface) == bytes:
        surface = Surface3D()
        surface.ParseFromString(pb_surface)
    else:
        surface = pb_surface
    vertices = [[v.x, v.y, v.z] for v in surface.vertices]
    faces = [[f.v0, f.v1, f.v2] for f in surface.faces]
    cells = [("triangle", faces)]
    mesh = meshio.Mesh(vertices, cells)
    if len(surface.normals) > 0:
        normals = np.array([[n.x, n.y, n.z] for n in surface.normals])
        mesh.cell_data["normals"] = normals
    meshio.write(path, mesh)

def save_3d_volume_mesh_with_meshio(path, pb_mesh):
    if type(pb_mesh) == bytes:
        volume_mesh = Mesh3D()
        volume_mesh.ParseFromString(pb_mesh)
    else:
        volume_mesh = pb_mesh
    vertices = [[v.x, v.y, v.z] for v in volume_mesh.vertices]
    cells = [[c.v0, c.v1, c.v2, c.v3] for c in volume_mesh.cells]

    cells = [("tetra", cells)]
    mesh = meshio.Mesh(vertices, cells)
    meshio.write(path, mesh)
