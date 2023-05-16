from dtcc_model import Raster

from . import interpolation
from . import stats

Raster.add_processors(interpolation)
Raster.add_processors(stats)