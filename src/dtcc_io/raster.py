import rasterio
from rasterio.transform import from_origin
import os
import numpy as np
from pathlib import Path
from PIL import Image

from . import generic

from dtcc_model import Raster
from .logging import info, error, warning


def _load_proto_raster(path, **kwargs):
    raster = Raster()
    raster.from_proto(path.read_bytes())
    return raster


def _load_rasterio(path, **kwargs):
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


def _load_csv(path, delimiter=",", **kwargs):
    raster = Raster()
    data = np.loadtxt(path, delimiter=delimiter)
    raster.data = data
    return raster


def load(path, delimiter=",") -> Raster:
    """
    Load a raster file as a `Raster` object.

    Args:
        path (str): The path to the raster file.
        delimiter (str): The delimiter used in case of a CSV file (default ",").

    Returns:
        Raster: A `Raster` object representing the raster file loaded.
    """
    path = Path(path)
    return generic.load(path, "raster", Raster, _load_formats, delimiter=delimiter)


def _save_proto_raster(raster, path):
    path.write_bytes(raster.to_proto().SerializeToString())


def _save_json_raster(raster, path):
    path.write_text(raster.to_json())


def _save_geotif(raster, path):
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


def _save_image(raster, path):
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


def _save_csv(raster, path):
    np.savetxt(path, raster.data, delimiter=",")
    return True


def save(raster: Raster, path):
    """
    Save a `Raster` object to a file.

    Parameters
    ----------
    raster : Raster
        The `Raster` object to save.
    path : str
        The path to the output file.
    """

    path = Path(path)
    return generic.save(raster, path, "raster", _save_formats)


_load_formats = {
    Raster: {
        ".pb": _load_proto_raster,
        ".pb2": _load_proto_raster,
        ".tif": _load_rasterio,
        ".geotif": _load_rasterio,
        ".png": _load_rasterio,
        ".asc": _load_rasterio,
        ".csv": _load_csv,
        ".txt": _load_csv,
    }
}

_save_formats = {
    Raster: {
        ".pb": _save_proto_raster,
        ".pb2": _save_proto_raster,
        ".json": _save_json_raster,
        ".tif": _save_geotif,
        ".png": _save_image,
        ".jpg": _save_image,
        ".csv": _save_csv,
    }
}
