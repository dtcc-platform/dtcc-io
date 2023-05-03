from dtcc_model import PointCloud

from . import filters
from . import convert

PointCloud.add_processors(filters)
PointCloud.add_processors(convert)
