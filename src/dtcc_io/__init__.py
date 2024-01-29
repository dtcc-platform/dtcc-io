from . import pointcloud
from . import meshes
from . import city
from . import landuse
from . import roadnetwork
from . import raster
from . import info
from .cityjson import cityjson

load_pointcloud = pointcloud.load
save_pointcloud = pointcloud.save

load_raster = raster.load
save_raster = raster.save

load_mesh = meshes.load_mesh
load_volume_mesh = meshes.load_volume_mesh
save_mesh = meshes.save
save_volume_mesh = meshes.save
list_mesh_io = meshes.list_io
print_mesh_io = meshes.print_io

load_city = city.load
save_city = city.save

load_city = city.load
save_city = city.save
load_footprints = city.load
save_footprints = city.save

load_landuse = landuse.load

load_roadnetwork = roadnetwork.load
save_roadnetwork = roadnetwork.save

load_cityjson = cityjson.load

from dtcc_model import City, PointCloud, Raster, Mesh, VolumeMesh, RoadNetwork

City.add_methods(save_city, "save")
PointCloud.add_methods(save_pointcloud, "save")
Raster.add_methods(save_raster, "save")
Mesh.add_methods(save_mesh, "save")
VolumeMesh.add_methods(save_mesh, "save")
RoadNetwork.add_methods(save_roadnetwork, "save")


__all__ = [
    "load_mesh",
    "save_mesh",
    "load_volume_mesh",
    "save_volume_mesh",
    "load_pointcloud",
    "save_pointcloud",
    "load_raster",
    "save_raster",
    "load_city",
    "save_city",
    "load_footprints",
    "save_footprints",
    "load_landuse",
    "load_roadnetwork",
    "save_roadnetwork",
]
