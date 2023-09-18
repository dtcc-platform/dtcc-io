import laspy
import fiona
import meshio
import rasterio
import numpy as np
from pathlib import Path
from types import UnionType
from dtcc_model import Bounds


def las_file_bounds(las_file):
    """
    Calculate the bounding box of a LAS file without loading it.

    Args:
        las_file (str): The path to the LAS file.

    Returns:
        Bounds: A `Bounds` object representing the bounding box of the LAS file.
    """
    src = laspy.read(las_file)
    bounds = Bounds(
        src.header.x_min, src.header.y_min, src.header.x_max, src.header.y_max
    )
    return bounds


def _las_pointcloud_info(path: [str | Path]) -> dict:
    info = {}
    info["bounds"] = las_file_bounds(path)
    src = laspy.read(path)
    info["crs"] = src.header.parse_crs().name
    info["x_min"], info["x_max"] = src.header.x_min, src.header.x_max
    info["y_min"], info["y_max"] = src.header.y_min, src.header.y_max
    info["z_min"], info["z_max"] = src.header.z_min, src.header.z_max
    info["count"] = src.header.point_count

    return info


def _csv_pointcloud_info(path: [str | Path]) -> dict:
    try:
        pts = np.loadtxt(path, delimiter=",")
    except ValueError:
        raise ValueError(f"File {path} is not a valid CSV pointcloud file")
    info = {}
    info["points"] = pts.shape[0]
    info["x_min"], info["x_max"] = pts[:, 0].min(), pts[:, 0].max()
    info["y_min"], info["y_max"] = pts[:, 1].min(), pts[:, 1].max()
    info["z_min"], info["z_max"] = pts[:, 2].min(), pts[:, 2].max()
    return info


def info_pointcloud(path: [str | Path]) -> dict:
    """
    Print information about a LAS file.
    Args:
        path: the path to the LAS file.

    Returns:
        a dictionary containing information about the LAS file.
    """

    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")
    if not path.is_file():
        raise ValueError(f"Path {path} is not a file")
    if path.suffix in [".las", ".laz"]:
        info = _las_pointcloud_info(path)
    elif path.suffix in [".csv", ".txt"]:
        info = _csv_pointcloud_info(path)
    else:
        raise ValueError(f"File {path} is not a supported pointcloud format")

    info["type"] = "pointcloud"
    info["path"] = str(path)

    return info


def info_vector(path: [str | Path]) -> dict:
    """
    Print information about a vector file.
    Args:
        path: the path to the vector file.

    Returns:
        a dictionary containing information about the vector file.
    """

    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")
    if not path.is_file():
        raise ValueError(f"Path {path} is not a file")
    try:
        f = fiona.open(path)
        f.close()
    except fiona.errors.DriverError:
        raise ValueError(f"File {path} is not a supported vector file format")

    info = {}
    info["path"] = str(path)
    info["type"] = "vector"
    with fiona.open(path) as src:
        info["crs"] = src.crs.to_string()
        info["count"] = len(src)
        info["x_min"], info["x_max"] = src.bounds[0], src.bounds[2]
        info["y_min"], info["y_max"] = src.bounds[1], src.bounds[3]
        info["geometry_type"] = src.schema["geometry"]

    return info


def info_raster(path: [str | Path]) -> dict:
    """
    Print information about a raster file.
    Args:
        path: the path to the raster file.

    Returns:
        a dictionary containing information about the raster file.
    """

    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")
    if not path.is_file():
        raise ValueError(f"Path {path} is not a file")
    try:
        f = rasterio.open(path)
    except rasterio.errors.RasterioIOError:
        raise ValueError(f"File {path} is not a supported raster file format")

    info = {}
    info["path"] = str(path)
    info["type"] = "raster"
    crs = f.crs
    if crs is not None:
        info["crs"] = crs.to_string()
    else:
        info["crs"] = ""
    info["height"] = f.height
    info["width"] = f.width
    info["cell_size"] = f.res[0]
    info["x_min"], info["x_max"] = f.bounds.left, f.bounds.right
    info["y_min"], info["y_max"] = f.bounds.bottom, f.bounds.top
    info["nodata"] = f.nodata
    info["channels"] = f.count

    return info


def info_mesh(path: [str | Path]) -> dict:
    """
    Print information about a mesh file.
    Args:
        path: the path to the mesh file.

    Returns:
        a dictionary containing information about the mesh file.
    """
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")
    if not path.is_file():
        raise ValueError(f"Path {path} is not a file")
    try:
        mesh = meshio.read(path)
    except ValueError:
        raise ValueError(f"File {path} is not a supported mesh file format")

    info = {}
    info["path"] = str(path)
    info["type"] = "mesh"
    info["crs"] = ""
    info["vertices"] = mesh.points.shape[0]
    info["faces"] = mesh.cells[0].data.shape[0]
    info["x_min"], info["x_max"] = mesh.points[:, 0].min(), mesh.points[:, 0].max()
    info["y_min"], info["y_max"] = mesh.points[:, 1].min(), mesh.points[:, 1].max()
    info["z_min"], info["z_max"] = mesh.points[:, 2].min(), mesh.points[:, 2].max()

    return info
