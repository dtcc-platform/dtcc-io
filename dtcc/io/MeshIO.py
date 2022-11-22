import pyassimp
import pyassimp.postprocess
import numpy as np
from dtcc_model.protobuf.dtcc_pb2 import Mesh2D, Mesh3D, Surface2D, Surface3D, Simplex2D, Simplex3D, Vector2D, Vector3D

def read(path, return_serialized=True):
    scene = pyassimp.load(path, pyassimp.postprocess.aiProcess_Triangulate)
    for mesh in scene.meshes:
        if mesh.vertices.shape[1] == 3:
            if mesh.faces.shape[1] == 3:
                return read_3d_surface(mesh, return_serialized)
            else:
                raise NotImplementedError("Only triangular surface meshes are supported")
        else:
            print(f"Cannot read mesh with {mesh.vertices.shape[1]} dimensions")

def read_3d_surface(mesh, return_serialized):
    pb = Surface3D()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=v[2]) for v in mesh.vertices])
    pb.faces.extend([Simplex2D(v0=f[0], v1=f[1], v2=f[2]) for f in mesh.faces])
    if mesh.normals is not None:
        pb.normals.extend([Vector3D(x=n[0], y=n[1], z=n[2]) for n in mesh.normals])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb

def write(path, pb_mesh):
    write_3d_surface(path, pb_mesh)

def write_3d_surface(path, pb_surface):
    if type(pb_surface) == bytes:
        surface = Surface3D()
        surface.ParseFromString(surface)
    else:
        surface = pb_surface
    vertices = np.array([[v.x, v.y, v.z] for v in surface.vertices])
    faces = np.array([[f.v0, f.v1, f.v2] for f in surface.faces])
    if len(surface.normals) > 0:
        normals = np.array([[n.x, n.y, n.z] for n in surface.normals])
    pyassimp.export_mesh(path, vertices, faces, normals)
    