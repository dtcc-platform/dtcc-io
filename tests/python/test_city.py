import unittest

import tempfile
import json
from pathlib import Path

import dtcc_io as io


class TestCity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.building_shp_file = str(
            (
                Path(__file__).parent
                / ".."
                / "data"
                / "MinimalCase"
                / "PropertyMap.shp"
            ).resolve()
        )

    def test_load_shp_buildings(self):
        cm = io.load_footprints(self.building_shp_file, "uuid")
        self.assertEqual(len(cm.buildings), 5)
        cm2 = io.load_footprints(self.building_shp_file, "uuid", area_filter=36)
        self.assertEqual(len(cm2.buildings), 4)

    def test_read_crs(self):
        cm = io.load_footprints(self.building_shp_file)
        self.assertEqual(cm.georef.crs.lower(), "epsg:3857")

    def test_buildings_bounds(self):
        bounds = io.city.building_bounds(self.building_shp_file)
        self.assertAlmostEqual(bounds.xmin, -5.14247442, places=3)
        self.assertAlmostEqual(bounds.ymin, -15.975332, places=3)
        self.assertAlmostEqual(bounds.xmax, 12.9899332, places=3)
        self.assertAlmostEqual(bounds.ymax, -1.098147, places=3)

    def test_buildings_bounds_buffered(self):
        bounds = io.city.building_bounds(self.building_shp_file, 5)
        self.assertAlmostEqual(bounds.xmin, -5.14247442 - 5, places=3)
        self.assertAlmostEqual(bounds.ymin, -15.975332 - 5, places=3)
        self.assertAlmostEqual(bounds.xmax, 12.9899332 + 5, places=3)
        self.assertAlmostEqual(bounds.ymax, -1.098147 + 5, places=3)

    def test_save_city(self):
        city = io.load_footprints(self.building_shp_file, "uuid")
        outfile = tempfile.NamedTemporaryFile(suffix=".geojson")
        city.save(outfile.name)
        with open(outfile.name) as f:
            data = json.load(f)
        self.assertEqual(len(data["features"]), 5)

    def test_protobuf(self):
        city = io.load_footprints(self.building_shp_file, "uuid")
        outfile = tempfile.NamedTemporaryFile(suffix=".pb")
        outfile_name = outfile.name
        outfile.close()
        city.save(outfile_name)
        city2 = io.load_footprints(outfile_name)
        self.assertEqual(len(city2.buildings), 5)


if __name__ == "__main__":
    unittest.main()
