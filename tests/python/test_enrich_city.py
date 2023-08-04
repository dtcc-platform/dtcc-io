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
        city = dtcc_io.load_footprints(building_shp_file, "uuid")
        pc = dtcc_io.load_pointcloud(point_cloud_file)
        print(city.bounds)
        print(pc)
        self.assertEqual(city.terrain.shape, ())
        city = city.terrain_from_pointcloud(pc, cell_size=1, ground_only=False)
        self.assertEqual(city.terrain.shape, (23, 19))
        self.assertAlmostEqual(city.terrain.data[0, 0], 1.0)


if __name__ == "__main__":
    unittest.main()
