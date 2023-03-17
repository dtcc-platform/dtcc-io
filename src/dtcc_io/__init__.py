import dtcc_io.bounds as bounds
import dtcc_io.citymodel as citymodel
import dtcc_io.elevationmodel as elevationmodel
import dtcc_io.mesh as mesh
import dtcc_io.pointcloud as pointcloud

read_mesh = mesh.read
write_mesh = mesh.write
read_pointcloud = pointcloud.read
write_pointcloud = pointcloud.write
read_citymodel = citymodel.read
write_citymodel = citymodel.write
read_elevationmodel = elevationmodel.read
write_elevationmodel = elevationmodel.write

__all__ = ['bounds', 'citymodel', 'elevationmodel', 'mesh', 'pointcloud']
