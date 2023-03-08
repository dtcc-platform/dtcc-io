import pyassimp
import pyassimp.postprocess
import meshio
import numpy as np

from dtcc_model import Vector3D, Simplex2D, Surface3D, Mesh3D


def read(path, triangulate=False, return_serialized=False):
    path = str(path)
    suffix = path.split(".")[-1].lower()
    reader_libs = {
        "obj": read_with_meshio,
        "ply": read_with_meshio,
        "stl": read_with_meshio,
        "vtk": read_with_meshio,
        "vtu": read_with_meshio,

        "dae": read_with_assimp,
        "fbx": read_with_assimp,
        "gltf": read_with_assimp,
        "glb": read_with_assimp
    }
    print(f"Reading mesh from {path}")
    if suffix in reader_libs:
        pb = reader_libs[suffix](path, return_serialized=return_serialized)
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
    #         return read_3d_surface(mesh, return_serialized)
    #     else:
    #         raise NotImplementedError(
    #             "Only triangular surface meshes are supported"
    #         )
    # else:
    #     print(f"Cannot read mesh with {mesh.vertices.shape[1]} dimensions")


def read_with_assimp(path, return_serialized=False):
    scene = pyassimp.load(path, pyassimp.postprocess.aiProcess_Triangulate)
    print(f"Loaded {len(scene.meshes)} meshes")
    mesh = scene.meshes[0]
    print(mesh)
    print(mesh.vertices.shape)
    print(mesh.faces.shape)
    return create_3d_surface(mesh.vertices, mesh.faces, mesh.normals, return_serialized=return_serialized)


def read_with_meshio(path, return_serialized=False):
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


def write(path, pb_mesh, volume_mesh=False):
    path = str(path)
    if not volume_mesh:
        writer_libs = {
            "obj": write_3d_surface_with_meshio,
            "ply": write_3d_surface_with_meshio,
            "stl": write_3d_surface_with_meshio,
            "vtk": write_3d_surface_with_meshio,
            "vtu": write_3d_surface_with_meshio,
        }
    if volume_mesh:
        writer_libs = {
            "vtk": write_3d_volume_mesh_with_meshio,
            "vtu": write_3d_volume_mesh_with_meshio,
        }
    suffix = path.split(".")[-1].lower()
    if suffix in writer_libs:
        writer_libs[suffix](path, pb_mesh)
    else:
        raise ValueError(
            f"Unknown file format: {suffix}, supported formats are: {list(writer_libs.keys())}")


def write_3d_surface_with_meshio(path, pb_surface):
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
        normals = [[n.x, n.y, n.z] for n in surface.normals]
        mesh.cell_data["normals"] = normals
    meshio.write(path, mesh)

def write_3d_volume_mesh_with_meshio(path, pb_mesh):
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
