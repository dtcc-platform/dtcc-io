import dtcc_io.bounds as bounds
import dtcc_io.citymodel as citymodel
import dtcc_io.elevationmodel as elevationmodel
import dtcc_io.mesh.mesh as mesh
import dtcc_io.pointcloud as pointcloud
import dtcc_io.view as view

read_surface3d = mesh.load_surface3d
write_surface3d = mesh.save_surface3d
load_surface3d = mesh.load_surface3d
save_surface3d = mesh.save_surface3d
load_mesh = mesh.load_surface3d
save_mesh = mesh.save_surface3d

load_mesh3d = mesh.load_mesh3d
save_mesh3d = mesh.save_mesh3d

save_mesh2d = mesh.save_mesh2d

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

view_citymodel = view.view_citymodel
__all__ = ['bounds', 'citymodel', 'elevationmodel', 'mesh', 'pointcloud']
