import pyassimp
import pyassimp.postprocess

from dtcc_io.mesh.utils import create_3d_surface

def load_with_assimp(path, return_serialized=False, mesh_type="surface"):
    path = str(path)
    scene = pyassimp.load(path, pyassimp.postprocess.aiProcess_Triangulate)
    print(f"Loaded {len(scene.meshes)} meshes")
    mesh = scene.meshes[0]
    print(mesh)
    print(mesh.vertices.shape)
    print(mesh.faces.shape)
    return create_3d_surface(
        mesh.vertices, mesh.faces, mesh.normals, return_serialized=return_serialized
    )