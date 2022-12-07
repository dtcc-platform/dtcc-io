import unittest

from pathlib import Path

from dtcc.io import PointCloudIO


class TestPointcloud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.building_las_file = str(
            (
                Path(__file__).parent / ".." / "data" / "MinimalCase" / "pointcloud.las"
            ).resolve()
        )

    def test_load_pointcloud(self):
        pc = PointCloudIO.read(self.building_las_file, return_serialized=False)
        self.assertEqual(len(pc.points), 8148)
        self.assertEqual(len(pc.classification), 8148)
        self.assertEqual(len(pc.usedClassifications), 2)

    def test_point_cloud_bounds(self):
        bounds = PointCloudIO.calc_las_bounds(self.building_las_file)
        self.assertAlmostEqual(bounds[0], -8.01747, places=3)
        self.assertAlmostEqual(bounds[1], -18.850332, places=3)
        self.assertAlmostEqual(bounds[2], 15.92373, places=3)
        self.assertAlmostEqual(bounds[3], 1.83826, places=3)
        


if __name__ == "__main__":
    unittest.main()
