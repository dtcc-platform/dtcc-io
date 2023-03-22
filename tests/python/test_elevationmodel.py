import unittest

from pathlib import Path

import numpy as np
import os, tempfile
import dtcc_io as io

class TestMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dem_raster = str(
            (Path(__file__).parent / ".." / "data" / "testraster.tif").resolve()
        )

    def test_load_elevation_model(self):
        em = io.read_elevationmodel(self.dem_raster, return_serialized=False)
        self.assertEqual(em.grid.xStep, 0.5)
        self.assertEqual(em.grid.xSize, 50)
        self.assertEqual(em.grid.ySize, 50)
        self.assertEqual(em.values[0], 0.5)
        self.assertEqual(em.values[-1], (50 * 50) * 0.5)

    def test_to_array(self):
        em = io.read_elevationmodel(self.dem_raster, return_serialized=False)
        data = io.elevationmodel.to_array(em)
        self.assertIsInstance(data,np.ndarray)
        self.assertEqual(data.shape, (50,50))

    def test_write_elevation_model(self):
        em = io.load_elevationmodel(self.dem_raster, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".tif", delete=False).name
        io.save_elevationmodel(outfile, em)
        em = io.load_elevationmodel(outfile, return_serialized=False)
        self.assertEqual(em.grid.xStep, 0.5)
        os.unlink(outfile)
    

if __name__ == "__main__":
    unittest.main()