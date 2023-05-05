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


class TestResample(unittest.TestCase):
    def test_upscale(self):
        dem = io.load_raster("data/test_dem.tif")
        orig_height = dem.height
        orig_width = dem.width
        dem = dem.resample(scale=2)
        self.assertEqual(dem.height, orig_height * 2)
        self.assertEqual(dem.width, orig_width * 2)

    def test_downscale(self):
        dem = io.load_raster("data/test_dem.tif")
        orig_height = dem.height
        orig_width = dem.width
        dem = dem.resample(scale=0.5)
        self.assertEqual(dem.height, orig_height // 2)
        self.assertEqual(dem.width, orig_width // 2)

    def test_resample_nearest(self):
        dem = io.load_raster("data/test_dem.tif")
        dem = dem.resample(scale=4, method="nearest")
        self.assertEqual(dem.data[0, 0], dem.data[0, 1])
        self.assertEqual(dem.data[0, 0], dem.data[1, 0])
        self.assertEqual(dem.data[0, 0], dem.data[1, 1])
        self.assertEqual(dem.data[0, 0], dem.data[2, 2])
