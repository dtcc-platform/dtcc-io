# Playground for testing

from dtcc_model import *
from dtcc_io import *

logging.set_log_level("DEBUG")

mesh = Mesh()
volume_mesh = VolumeMesh()

save_mesh(mesh, "mesh.obj")
# save_mesh(volume_mesh, "volume_mesh.obj")

list_mesh_io()
print_mesh_io()

f0 = MeshField()
f1 = MeshVectorField()
f2 = VolumeMeshField()
f3 = VolumeMeshVectorField()

# save_field(f0, "f0.vtu")
# save_field(f1, "f1.vtu")
# save_field(f2, "f2.vtu")
# save_field(f3, "f3.vtu")
