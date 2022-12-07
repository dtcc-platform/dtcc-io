import unittest

from pathlib import Path

from dtcc.io import CityModelIO

class TestCityModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.building_shp_file = str(
            (
                Path(__file__).parent
                / ".."
                / "data"
                / "MinimalCase"
                / "propertyMap.shp"
            ).resolve()
        )

    def test_load_shp_buildings(self):
        cm = CityModelIO.read(self.building_shp_file, "uuid")
        self.assertEqual(len(cm.buildings), 5)
        cm2 = CityModelIO.read(self.building_shp_file, "uuid", area_filter=36)
        self.assertEqual(len(cm2.buildings), 4)
    
    def test_buildings_bounds(self):
        bounds = CityModelIO.building_bounds(self.building_shp_file)
        self.assertAlmostEquals(bounds[0], -5.14247442, places=3)
        self.assertAlmostEquals(bounds[1], -15.975332, places=3)
        self.assertAlmostEquals(bounds[2], 12.9899332, places=3)
        self.assertAlmostEquals(bounds[3], -1.098147, places=3)

    def test_buildings_bounds_buffered(self):
        bounds = CityModelIO.building_bounds(self.building_shp_file,5)
        self.assertAlmostEquals(bounds[0], -5.14247442-5, places=3)
        self.assertAlmostEquals(bounds[1], -15.975332-5, places=3)
        self.assertAlmostEquals(bounds[2], 12.9899332+5, places=3)
        self.assertAlmostEquals(bounds[3], -1.098147+5, places=3)

if __name__ == "__main__":
    unittest.main()