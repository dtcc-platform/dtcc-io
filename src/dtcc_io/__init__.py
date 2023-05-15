# FIXME: Use Bounds class from dtcc-model
import dtcc_io.bounds as bounds
import dtcc_io.citymodel as citymodel
import dtcc_io.raster as raster

import dtcc_io.process

from . import pointcloud
from . import meshes
from . import fields
from . import citymodel
from . import landuse

load_pointcloud = pointcloud.load
save_pointcloud = pointcloud.save

load_raster = raster.load
save_raster = raster.save

load_mesh = meshes.load_mesh
load_volume_mesh = meshes.load_volume_mesh
save_mesh = meshes.save
list_mesh_io = meshes.list_io
print_mesh_io = meshes.print_io

load_mesh_field = fields.load_field
load_mesh_vector_field = fields.load_vector_field
save_field = fields.save
list_field_io = fields.list_io
print_field_io = fields.print_io

load_citymodel = citymodel.load
save_citymodel = citymodel.save

# FIXME: Move to fields
import dtcc_io.gridfield as gridfield

load_gridfield = gridfield.load
save_gridfield = gridfield.save

load_citymodel = citymodel.load
save_citymodel = citymodel.save
load_footprints = citymodel.load
save_footprints = citymodel.save

load_landuse = landuse.load

from dtcc_model import CityModel, PointCloud, Raster, Mesh, VolumeMesh

CityModel.add_processors(save_citymodel, "save")
PointCloud.add_processors(save_pointcloud, "save")
Raster.add_processors(save_raster, "save")
Mesh.add_processors(save_mesh, "save")
VolumeMesh.add_processors(save_mesh, "save")

# __all__ = ['bounds', 'citymodel', 'elevationmodel', 'mesh', 'pointcloud']

# __all__ = [
#     "load_mesh",
#     "save_mesh",
#     "load_pointcloud",
#     "save_pointcloud",
#     "load_elevationmodel",
#     "save_elevationmodel",
#     "load_citymodel",
#     "save_citymodel",
#     "load_footprints",
#     "save_footprints",
#     "view_citymodel",
# ]
