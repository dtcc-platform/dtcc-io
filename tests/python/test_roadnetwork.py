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

    def test_vertices(self):
        rn = io.load_roadnetwork(self.roadnetwork_shp_file, type_field="KATEGORI")
        r0 = rn.roads[0]
        self.assertEqual(len(r0.road_vertices), len(r0.road_geometry.coords))
        r123 = rn.roads[123]
        self.assertEqual(len(r123.road_vertices), len(r123.road_geometry.coords))

        verts = rn.vertices[r0.road_vertices]
        self.assertAlmostEqual(
            verts[0][0], list(r0.road_geometry.coords)[0][0], places=3
        )
        self.assertAlmostEqual(
            verts[0][1], list(r0.road_geometry.coords)[0][1], places=3
        )

        self.assertAlmostEqual(
            verts[12][0], list(r0.road_geometry.coords)[12][0], places=3
        )
        self.assertAlmostEqual(
            verts[12][1], list(r0.road_geometry.coords)[12][1], places=3
        )

    def test_simplify(self):
        rn = io.load_roadnetwork(self.roadnetwork_shp_file, type_field="KATEGORI")
        rn_simplified = io.load_roadnetwork(
            self.roadnetwork_shp_file, type_field="KATEGORI", simplify=1
        )
        self.assertEqual(len(rn_simplified.roads), len(rn.roads))
        self.assertLess(len(rn_simplified.vertices), len(rn.vertices))

        ro_start = list(rn.roads[14].road_geometry.coords)[0]
        ro_end = list(rn.roads[14].road_geometry.coords)[-1]ß
        rs_start = list(rn_simplified.roads[14].road_geometry.coords)[0]
        rs_end = list(rn_simplified.roads[14].road_geometry.coords)[-1]
        self.assertEqual(ro_start, rs_start)
        self.assertEqual(ro_end, rs_end)
