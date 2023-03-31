from dtcc_model import Surface3D, Vector3D, Simplex2D, Mesh3D, Simplex3D, Mesh2D, Simplex2D, Vector2D

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
    
def create_3d_volume_mesh(vertices, cells, return_serialized=False):
    pb = Mesh3D()
    pb.vertices.extend([Vector3D(x=v[0], y=v[1], z=v[2]) for v in vertices])
    pb.cells.extend([Simplex3D(v0=c[0], v1=c[1], v2=c[2], v3=c[3]) for c in cells])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb

def create_2d_mesh(vertices, faces, return_serialized=False):
    pb = Mesh2D()
    pb.vertices.extend([Vector2D(x=v[0], y=v[1]) for v in vertices])
    pb.faces.extend([Simplex2D(v0=f[0], v1=f[1], v2=f[2]) for f in faces])
    if return_serialized:
        return pb.SerializeToString()
    else:
        return pb

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