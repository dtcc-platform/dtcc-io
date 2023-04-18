import unittest

from pathlib import Path

import numpy as np
import os, tempfile
import dtcc_io as io


class TestGridField(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dem_raster = str(
            (Path(__file__).parent / ".." / "data" / "test_dem.tif").resolve()
        )

    def test_load_gridfield(self):
        em = io.load_gridfield(self.dem_raster)
        self.assertEqual(em.grid.shape, (40, 20))

    def test_get_height_width(self):
        em = io.load_gridfield(self.dem_raster)
        self.assertEqual(em.height, 40)
        self.assertEqual(em.width, 20)

    def test_get_cell_size(self):
        em = io.load_gridfield(self.dem_raster)
        self.assertEqual(em.cell_size, (2.0, 2.0))

    def test_write_elevation_model(self):
        em = io.load_gridfield(self.dem_raster)
        outfile = tempfile.NamedTemporaryFile(suffix=".tif", delete=False).name
        io.save_gridfield(em, outfile)
        em = io.load_gridfield(outfile)
        self.assertEqual(em.height, 40)
        self.assertEqual(em.width, 20)
        self.assertEqual(em.cell_size, (2.0, 2.0))
        os.unlink(outfile)


if __name__ == "__main__":
    unittest.main()
