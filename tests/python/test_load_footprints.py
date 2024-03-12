import unittest

import tempfile
import json
from pathlib import Path

import dtcc_io as io
from dtcc_model import Bounds
from dtcc_model import Building
from dtcc_model import GeometryType


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
        buildings = io.load_footprints(self.building_shp_file, "uuid")
        self.assertEqual(len(buildings), 5)
        self.assertTrue(all([isinstance(b, Building) for b in buildings]))

    def test_load_with_area_filter(self):
        buildings = io.load_footprints(self.building_shp_file, "uuid", area_filter=36)
        self.assertEqual(len(buildings), 4)

    def test_load_with_bounds_filter(self):
        buildings = io.load_footprints(
            self.building_shp_file,
            "uuid",
            bounds=Bounds(-7, -18, 9, -5),
            min_edge_distance=0,
        )
        self.assertEqual(len(buildings), 1)

    def test_load_with_bounds_filter(self):
        buildings = io.load_footprints(
            self.building_shp_file,
            "uuid",
            bounds=Bounds(-7, -18, 15, 0),
            min_edge_distance=0,
        )
        self.assertEqual(len(buildings), 5)

    def test_read_crs(self):
        buildings = io.load_footprints(self.building_shp_file)
        building = buildings[2]
        srs = building.geometry[GeometryType.LOD0].transform.srs
        self.assertEqual(srs.upper(), "EPSG:3857")

    def test_buildings_bounds(self):
        bounds = io.footprints.building_bounds(self.building_shp_file)
        self.assertAlmostEqual(bounds.xmin, -5.14247442, places=3)
        self.assertAlmostEqual(bounds.ymin, -15.975332, places=3)
        self.assertAlmostEqual(bounds.xmax, 12.9899332, places=3)
        self.assertAlmostEqual(bounds.ymax, -1.098147, places=3)

    def test_buildings_bounds_buffered(self):
        bounds = io.footprints.building_bounds(self.building_shp_file, 5)
        self.assertAlmostEqual(bounds.xmin, -5.14247442 - 5, places=3)
        self.assertAlmostEqual(bounds.ymin, -15.975332 - 5, places=3)
        self.assertAlmostEqual(bounds.xmax, 12.9899332 + 5, places=3)
        self.assertAlmostEqual(bounds.ymax, -1.098147 + 5, places=3)

    # def test_save_footprints(self):
    #     city = io.load_footprints(self.building_shp_file, "uuid")
    #     outfile = tempfile.NamedTemporaryFile(suffix=".geojson")
    #     city.save(outfile.name)
    #     with open(outfile.name) as f:
    #         data = json.load(f)
    #     self.assertEqual(len(data["features"]), 5)


if __name__ == "__main__":
    unittest.main()
