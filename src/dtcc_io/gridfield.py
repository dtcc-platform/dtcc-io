import rasterio
from rasterio.transform import from_origin
import os
import numpy as np
from pathlib import Path


from dtcc_model import GridField


def load(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".tif", ".tiff", ".geotif", ".asc"]:
        return load_rasterio(path)
    else:
        raise ValueError(f"Cannot read file with suffix {suffix}")
    return None


def load_rasterio(path):
    gridfield = GridField()
    with rasterio.open(path) as src:
        data = src.read()
        gridfield.grid = data[0, :, :]
        gridfield.transform = src.transform
        gridfield.crs = src.crs

    return gridfield


def save(gridfield, path):
    path = Path(path)
    suffix = path.suffix.lower()[1:]
    if suffix in ["tif", "tiff"]:
        return save_tiff(path, gridfield)
    else:
        raise ValueError(f"Cannot write file with suffix {suffix}")
    return None


def save_tiff(path, gridfield):
    data = gridfield.grid
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        transform=gridfield.transform,
    ) as dst:
        dst.write(data, 1)
