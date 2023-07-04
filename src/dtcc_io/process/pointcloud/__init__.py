from dtcc_model import PointCloud

from . import filters
from . import convert

PointCloud.add_methods(filters)
PointCloud.add_methods(convert)
