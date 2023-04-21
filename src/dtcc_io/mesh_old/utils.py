from dtcc_model import Mesh, VolumeMesh, Vector3D, Triangle, Tetrahedron


def create_3d_surface(vertices, faces, normals=None, return_serialized=False):
    pb = Mesh()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=v[2]) for v in vertices])
    pb.faces.extend([Triangle(v0=f[0], v1=f[1], v2=f[2]) for f in faces])
    if normals is not None:
        pb.normals.extend([Vector3D(x=n[0], y=n[1], z=n[2]) for n in normals])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb


def create_3d_volume_mesh(vertices, cells, return_serialized=False):
    pb = VolumeMesh()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=v[2]) for v in vertices])
    pb.cells.extend([Tetrahedron(v0=c[0], v1=c[1], v2=c[2], v3=c[3]) for c in cells])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb


def create_2d_mesh(vertices, faces, return_serialized=False):
    pb = Mesh()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=0) for v in vertices])
    pb.faces.extend([Triangle(v0=f[0], v1=f[1], v2=f[2]) for f in faces])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb
