import scipy.ndimage
import numpy as np
import rasterio


def fill_holes(raster):
    """Fill nodata holes in a raster using the nearest neighbour"""
    data = raster.data
    nodata = raster.nodata
    mask = data == nodata
    if np.any(mask):
        print(f"filling {mask.sum()} holes in raster")
        ind = scipy.ndimage.distance_transform_edt(
            mask, return_distances=False, return_indices=True
        )
        data = data[tuple(ind)]
    raster.data = data
    return raster


def resample(raster, cell_size=None, scale=None, method="bilinear"):
    sample_methods = {
        "bilinear": 1,
        "nearest": 0,
        "cubic": 3,
    }
    if cell_size is None and scale is None:
        raise ValueError("Either cell_size or scale must be specified")
    if not method in sample_methods:
        raise ValueError(
            f"Invalid resampling method, use one of {list(sample_methods.keys())}"
        )
    if cell_size is not None:
        scale = cell_size / raster.cell_size[0]
    if scale == 1:
        return raster
    raster.data = scipy.ndimage.zoom(
        raster.data, scale, order=sample_methods[method], mode="nearest", grid_mode=True
    )
    raster.georef *= raster.georef.scale(scale, scale)

    return raster
