from dtcc_model import Raster

from . import interpolation
from . import stats

Raster.add_methods(interpolation)
Raster.add_methods(stats)
