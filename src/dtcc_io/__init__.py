# FIXME: Use Bounds class from dtcc-model
import dtcc_io.bounds as bounds

from . import pointcloud
from . import meshes
from . import fields
from . import citymodel

load_pointcloud = pointcloud.load
save_pointcloud = pointcloud.save

load_mesh = meshes.load
save_mesh = meshes.save

load_field = fields.load
save_field = fields.save

load_citymodel = citymodel.load
save_citymodel = citymodel.save

# FIXME: Move to fields
import dtcc_io.gridfield as gridfield

load_gridfield = gridfield.load
save_gridfield = gridfield.save


# FIXME: Remove read/write, use load/save
read_pointcloud = pointcloud.load
write_pointcloud = pointcloud.save
read_citymodel = citymodel.load
write_citymodel = citymodel.save
load_citymodel = citymodel.load
save_citymodel = citymodel.save
load_footprints = citymodel.load
save_footprints = citymodel.save


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
