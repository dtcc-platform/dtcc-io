import unittest

import dtcc_io as io
from dtcc_model import PointCloud, Raster

pc = io.load_pointcloud("data/MinimalCase/pointcloud.las")
print(len(pc.points))


class TestConvertPointCloud(unittest.TestCase):
    def test_rasterize(self):
        dem = pc.rasterize(1, ground_only=False)
        self.assertIsInstance(dem, Raster)
        self.assertEqual(dem.data.shape, (24, 21))
        dem = pc.rasterize(0.5, ground_only=False)
        self.assertEqual(dem.data.shape, (48, 42))
