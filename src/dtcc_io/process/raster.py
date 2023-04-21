import scipy.ndimage
import numpy as np


def fill_holes(raster):
    """Fill holes in a raster using nearest neighbour interpolation."""
    data = raster.data
    nodata = raster.nodata
    mask = data == nodata
    if np.any(mask):
        ind = scipy.ndimage.distance_transform_edt(
            mask, return_distances=False, return_indices=True
        )
        data[tuple(ind)]
    raster.data = data
    return raster
