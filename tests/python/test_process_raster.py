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


class TestRasterStats(unittest.TestCase):
    def test_single_stat(self):
        dem = io.load_raster("data/test_dem.tif")
        cm = io.load_citymodel("data/MinimalCase/PropertyMap.shp")
        footprints = [b.footprint for b in cm.buildings]
        stats = dem.stats(footprints, ["mean"])
        self.assertEqual(stats[0], 0.0)
        self.assertIsNone(stats[3])

    def test_multiple_stats(self):
        dem = io.load_raster("data/test_dem.tif")
        cm = io.load_citymodel("data/MinimalCase/PropertyMap.shp")
        footprints = [b.footprint for b in cm.buildings]
        stats = dem.stats(footprints, ["mean", "min", "max"])
        self.assertEqual(stats[0]["min"], 0.0)
        self.assertEqual(stats[0]["max"], 0.0)
        self.assertIsNone(stats[3]["min"])
        self.assertIsNone(stats[3]["max"])
        self.assertAlmostEqual(stats[4]["mean"], 10.2666, 3)
        self.assertAlmostEqual(stats[4]["min"], 8.2, 3)
        self.assertAlmostEqual(stats[4]["max"], 13, 3)
