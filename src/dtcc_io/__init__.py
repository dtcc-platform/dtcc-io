import dtcc_io.bounds as bounds
import dtcc_io.citymodel as citymodel
import dtcc_io.raster as raster

# import dtcc_io.elevationmodel as elevationmodel
# import dtcc_io.mesh.mesh as mesh
import dtcc_io.pointcloud as pointcloud

# import dtcc_io.view as view


# load_mesh = mesh.load_surface3d
# save_mesh = mesh.save_surface3d
# load_volume_mesh = mesh.load_mesh3d
# save_volume_mesh = mesh.save_mesh3d

read_pointcloud = pointcloud.load
write_pointcloud = pointcloud.save
load_pointcloud = pointcloud.load
save_pointcloud = pointcloud.save

load_raster = raster.load
save_raster = raster.save

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
