from dtcc_io.process.pointcloud.convert import rasterize
from dtcc_model import City, PointCloud, Raster


def terrain_from_pointcloud(
    city: City,
    pc: PointCloud,
    cell_size: float,
    window_size=3,
    radius=0,
    ground_only=True,
) -> City:
    """Generate a terrain model from a pointcloud
    args:
        pc: PointCloud to use for terrain
        cell_size: float cell size in meters
        window_size: int window size for interpolation
        radius: float radius for interpolation
    returns:
        City

    """
    dem = rasterize(
        pc,
        cell_size,
        bounds=city.bounds,
        window_size=window_size,
        radius=radius,
        ground_only=ground_only,
    )
    city.terrain = dem
    return city
