import unittest

from pathlib import Path

import numpy as np
import os, tempfile
import dtcc_io as io


class TestGridField(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dem_raster = (
            Path(__file__).parent / ".." / "data" / "test_dem.tif"
        ).resolve()

        cls.rgb_img = (Path(__file__).parent / ".." / "data" / "14040.png").resolve()

    def test_load_dem(self):
        dem = io.load_raster(self.dem_raster)
        self.assertEqual(dem.width, 20)
        self.assertEqual(dem.height, 40)
        self.assertEqual(dem.channels, 1)

    def test_load_image(self):
        image = io.load_raster(self.rgb_img)
        self.assertEqual(image.width, 228)
        self.assertEqual(image.height, 230)
        self.assertEqual(image.channels, 3)

    def test_get_cell_size(self):
        em = io.load_raster(self.dem_raster)
        self.assertEqual(em.cell_size, (2.0, -2.0))

    def test_get_cell_size_wld_file(self):
        em = io.load_raster(self.rgb_img)
        self.assertEqual(em.cell_size, (0.08, -0.08))

    def test_write_elevation_model(self):
        em = io.load_raster(self.dem_raster)
        outfile = tempfile.NamedTemporaryFile(suffix=".tif", delete=False).name
        io.save_raster(em, outfile)
        em = io.load_raster(outfile)
        self.assertEqual(em.height, 40)
        self.assertEqual(em.width, 20)
        self.assertEqual(em.cell_size, (2.0, -2.0))
        os.unlink(outfile)


if __name__ == "__main__":
    unittest.main()
