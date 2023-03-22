import rasterio
from rasterio.transform import from_origin
import os
import numpy as np
from pathlib import Path

from dtcc_model import Grid2D, Vector2D, GridField2D, BoundingBox2D


def load(path, return_serialized=False):

    path = Path(path)
    suffix = path.suffix.lower()[1:]
    if suffix in ["tif", "tiff"]:
        return load_tiff(path, return_serialized=return_serialized)
    else:
        raise ValueError(f"Cannot read file with suffix {suffix}")
    return None


def load_tiff(path, return_serialized=False):
    with rasterio.open(path) as src:
        data = src.read()
        data = data[0, :, :]
        grid = Grid2D()
        boundingbox = BoundingBox2D()
        boundingbox.p.CopyFrom(
            Vector2D(x=src.bounds.left, y=src.bounds.bottom))
        boundingbox.q.CopyFrom(Vector2D(x=src.bounds.right, y=src.bounds.top))
        grid.boundingBox.CopyFrom(boundingbox)
        grid.ySize = src.height
        grid.xSize = src.width
        grid.yStep = src.res[0]
        grid.xStep = src.res[1]

        gridfield = GridField2D()
        gridfield.grid.CopyFrom(grid)
        gridfield.values.extend(data.flatten().tolist())
    if return_serialized:
        return gridfield.SerializeToString()
    else:
        return gridfield


def to_array(gridfield):
    grid = gridfield.grid
    return np.array(gridfield.values).reshape(grid.ySize, grid.xSize)


def save(path, gridfield):
    path = Path(path)
    suffix = path.suffix.lower()[1:]
    if suffix in ["tif", "tiff"]:
        return save_tiff(path, gridfield)
    else:
        raise ValueError(f"Cannot write file with suffix {suffix}")
    return None


def save_tiff(path, gridfield):
    data = to_array(gridfield)
    grid = gridfield.grid
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=grid.ySize,
        width=grid.xSize,
        count=1,
        dtype=data.dtype,
        transform=from_origin(
            grid.boundingBox.p.x,
            grid.boundingBox.q.y,
            grid.xStep,
            grid.yStep,
        ),
    ) as dst:
        dst.write(data, 1)
