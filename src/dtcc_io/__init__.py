import dtcc_io.bounds as bounds
import dtcc_io.citymodel as citymodel
import dtcc_io.elevationmodel as elevationmodel
import dtcc_io.mesh as mesh
import dtcc_io.pointcloud as pointcloud

read_mesh = mesh.load
write_mesh = mesh.save
load_mesh = mesh.load
save_mesh = mesh.save

read_pointcloud = pointcloud.load
write_pointcloud = pointcloud.save
load_pointcloud = pointcloud.load
save_pointcloud = pointcloud.save

read_citymodel = citymodel.load
write_citymodel = citymodel.save
load_citymodel = citymodel.load
save_citymodel = citymodel.save
load_footprints = citymodel.load
save_footprints = citymodel.save

read_elevationmodel = elevationmodel.load
write_elevationmodel = elevationmodel.save
load_elevationmodel = elevationmodel.load
save_elevationmodel = elevationmodel.save

__all__ = ['bounds', 'citymodel', 'elevationmodel', 'mesh', 'pointcloud']
