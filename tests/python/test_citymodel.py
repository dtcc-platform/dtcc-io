import unittest

import tempfile
import json
from pathlib import Path

import dtcc_io as io

class TestCityModel(unittest.TestCase):
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
        self.assertEqual(cm.georeference.crs.lower(), "epsg:3857")
    
    def test_buildings_bounds(self):
        bounds = io.citymodel.building_bounds(self.building_shp_file)
        self.assertAlmostEqual(bounds[0], -5.14247442, places=3)
        self.assertAlmostEqual(bounds[1], -15.975332, places=3)
        self.assertAlmostEqual(bounds[2], 12.9899332, places=3)
        self.assertAlmostEqual(bounds[3], -1.098147, places=3)

    def test_buildings_bounds_buffered(self):
        bounds = io.citymodel.building_bounds(self.building_shp_file,5)
        self.assertAlmostEqual(bounds[0], -5.14247442-5, places=3)
        self.assertAlmostEqual(bounds[1], -15.975332-5, places=3)
        self.assertAlmostEqual(bounds[2], 12.9899332+5, places=3)
        self.assertAlmostEqual(bounds[3], -1.098147+5, places=3)

    def test_save_json(self):
        cm = io.load_footprints(self.building_shp_file, "uuid")
        outfile = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        outpath = Path(outfile.name)
        io.save_citymodel(cm, outfile.name)
        with open(outpath, "r") as f:
            json_data = json.load(f)
        self.assertEqual(len(json_data["buildings"]), 5)
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()