import unittest
from pathlib import Path

import dtcc_io as io


class TestProcessCityModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        building_shp_file = (
            Path(__file__).parent / ".." / "data" / "MinimalCase" / "PropertyMap.shp"
        ).resolve()

        landuse_shp_file = (
            Path(__file__).parent / ".." / "data" / "landuse_testdata.shp"
        ).resolve()

        cls.cm = io.load_footprints(building_shp_file, "uuid")
        cls.lu = io.load_landuse(landuse_shp_file, landuse_field="DETALJTYP")
        cls.cm.landuse = cls.lu

    def test_summerize_buildings(self):
        building_summary = self.cm.summerize_buildings(print_summary=False)
        self.assertEqual(building_summary["number"], 5)
        self.assertAlmostEqual(building_summary["total_area"], 118, places=0)

    def test_summerize_landuse(self):
        landuse_summary = self.cm.summerize_landuse(print_summary=True)
        self.assertTrue("GRASS" in landuse_summary)
        self.assertTrue("URBAN" in landuse_summary)
        self.assertTrue("WATER" in landuse_summary)
        self.assertAlmostEqual(landuse_summary["WATER"], 8042, places=0)
