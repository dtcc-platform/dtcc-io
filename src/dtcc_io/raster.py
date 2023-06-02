import rasterio
from rasterio.transform import from_origin
import os
import numpy as np
from pathlib import Path
from PIL import Image

from dtcc_model.raster import Raster
from .dtcc_logging import info, error, warning


def load(path):
    info(f"Loading raster from {path}")
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".tif", ".tiff", ".geotif", ".png", ".jpg", ".asc"]:
        return load_rasterio(path)
    else:
        raise ValueError(f"Cannot read file with suffix {suffix}")
    return None


def load_rasterio(path):
    raster = Raster()
    with rasterio.open(path) as src:
        data = src.read()
        data = data.squeeze()
        if data.ndim == 3:
            # rasterio returns (channels, height, width)
            # we want (width, heigh, channels)
            data = np.moveaxis(data, 0, -1)

        raster.data = np.squeeze(data)
        raster.georef = src.transform
        raster.crs = str(src.crs)

    return raster


def save(raster, path):
    info(f"Saving raster to {path}")
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".tif", ".tiff"]:
        return save_geotif(raster, path)
    elif suffix in [".png", ".jpg"]:
        return save_image(raster, path)
    else:
        raise ValueError(f"Cannot write file with suffix {suffix}")


def save_geotif(raster, path):
    data = raster.data
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=raster.height,
        width=raster.width,
        count=raster.channels,
        dtype=data.dtype,
        transform=raster.georef,
    ) as dst:
        if raster.channels == 1:
            dst.write(data, 1)
        else:
            dst.write(data, list(range(1, raster.channels + 1)))

    return True


def save_image(raster, path):
    suffix = path.suffix.lower()
    wld_suffix = f"{suffix[0]}{suffix[-1]}w"
    wld_path = path.with_suffix(wld_suffix)
    data = raster.data
    if raster.channels == 1:
        data = np.repeat(data[:, :, np.newaxis], 3, axis=2)
    with open(wld_path, "w") as f:
        f.write(
            f"{raster.georef.a}\n{raster.georef.b}\n{raster.georef.d}\n{raster.georef.e}\n{raster.georef.xoff}\n{raster.georef.yoff}"
        )
    im = Image.fromarray(data)
    im.save(path)
    return True
