import meshio
import numpy as np
from dtcc_io.mesh.utils import create_3d_surface
from dtcc_model import Mesh, VolumeMesh


def load_with_meshio(path, return_serialized=False, mesh_type="surface"):
    mesh = meshio.read(path)
    vertices = mesh.points
    faces = mesh.cells[0].data
    return create_3d_surface(vertices, faces, return_serialized=return_serialized)


def save_3d_surface_with_meshio(pb_surface, path):
    if type(pb_surface) == bytes:
        surface = Mesh()
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


def save_3d_volume_mesh_with_meshio(pb_mesh, path):
    if type(pb_mesh) == bytes:
        volume_mesh = VolumeMesh()
        volume_mesh.ParseFromString(pb_mesh)
    else:
        volume_mesh = pb_mesh
    vertices = [[v.x, v.y, v.z] for v in volume_mesh.vertices]
    cells = [[c.v0, c.v1, c.v2, c.v3] for c in volume_mesh.cells]

    cells = [("tetra", cells)]
    mesh = meshio.Mesh(vertices, cells)
    meshio.write(path, mesh)


def save_2d_surface_mesh_with_meshio(pb_mesh, path):
    if type(pb_mesh) == bytes:
        surface_mesh = Mesh()
        surface_mesh.ParseFromString(pb_mesh)
    else:
        surface_mesh = pb_mesh
    vertices = [[v.x, v.y, 0] for v in surface_mesh.vertices]
    faces = [[f.v0, f.v1, f.v2] for f in surface_mesh.faces]
    cells = [("triangle", faces)]
    mesh = meshio.Mesh(vertices, cells)
    meshio.write(path, mesh)
