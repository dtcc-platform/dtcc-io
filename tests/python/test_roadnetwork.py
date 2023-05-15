import unittest

import tempfile
import json
from pathlib import Path

import dtcc_io as io


class TestRoadnetworkIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roadnetwork_shp_file = (
            Path(__file__).parent / ".." / "data" / "road_network" / "test_road.shp"
        )

    def test_load_roadnetwork(self):
        rn = io.load_roadnetwork(self.roadnetwork_shp_file, type_field="KATEGORI")
        self.assertEqual(len(rn.roads), 244)

    def test_save_roadnetwork(self):
        rn = io.load_roadnetwork(self.roadnetwork_shp_file, type_field="KATEGORI")
        outfile = tempfile.NamedTemporaryFile(suffix=".geojson")
        rn.save(outfile.name)
        with open(outfile.name) as f:
            data = json.load(f)
        self.assertEqual(len(data["features"]), 244)
