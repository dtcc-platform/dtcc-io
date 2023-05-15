import unittest
from pathlib import Path

import dtcc_io as io


class TestLoadLanduse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.landuse_shp_file = str(
            (Path(__file__).parent / ".." / "data" / "landuse_testdata.shp").resolve()
        )

    def test_load_landuse(self):
        lu = io.load_landuse(self.landuse_shp_file, landuse_field="DETALJTYP")
        self.assertEqual(len(lu), 79)
        self.assertTrue("ADAT" in lu[0].properties)
