import unittest

import dtcc_io as io
from dtcc_model import Raster


class TestFillHoles(unittest.TestCase):
    def test_shape(self):
        dem = io.load_raster("data/test_dem.tif")
        dem = dem.fill_holes()
        self.assertEqual(dem.width, 20)
        self.assertEqual(dem.height, 40)
        self.assertEqual(dem.channels, 1)

    def test_fill_holes(self):
        dem = io.load_raster("data/test_dem.tif")
        dem.nodata = -9999
        dem.data[5, 5] = -9999
        self.assertEqual(dem.data[5, 5], -9999)
        dem = dem.fill_holes()
        self.assertGreater(dem.data[5, 5], 0)
