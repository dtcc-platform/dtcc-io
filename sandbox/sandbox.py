# Playground for testing

from dtcc_model import *
from dtcc_io import *

logging.set_log_level("DEBUG")

mesh = load_mesh("../tests/data/cube.stl")
volume_mesh = VolumeMesh()

print_mesh_io()

save_mesh(mesh, "mesh.stl")


f0 = MeshField()
f1 = MeshVectorField()
f2 = VolumeMeshField()
f3 = VolumeMeshVectorField()

print_field_io()

save_field(f0, "f0.vtu")
save_field(f1, "f1.vtu")
save_field(f2, "f2.vtu")
save_field(f3, "f3.vtu")
