import dtcc_io
import unittest
from pathlib import Path


class TestSetTerrain(unittest.TestCase):
    def test_create_terrain(self):
        building_shp_file = (
            Path(__file__).parent / ".." / "data" / "MinimalCase" / "PropertyMap.shp"
        ).resolve()

        point_cloud_file = (
            Path(__file__).parent / ".." / "data" / "MinimalCase" / "pointcloud.las"
        ).resolve()
        cm = dtcc_io.load_footprints(building_shp_file, "uuid")
        pc = dtcc_io.load_pointcloud(point_cloud_file)
        print(cm.bounds)
        print(pc)
        self.assertEqual(cm.terrain.shape, ())
        cm = cm.terrain_from_pointcloud(pc, cell_size=1, ground_only=False)
        self.assertEqual(cm.terrain.shape, (23, 20))
        self.assertAlmostEqual(cm.terrain.data[0, 0], 1.0)


if __name__ == "__main__":
    unittest.main()
