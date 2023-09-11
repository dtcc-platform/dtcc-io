import unittest
from dtcc_io import info


las_file = "data/MinimalCase/pointcloud.las"


class TestPointcloudInfo(unittest.TestCase):
    def test_numpoints(self):
        pc_info = info.pointcloud_info(las_file)
        self.assertEqual(pc_info["count"], 8148)

    def test_bounds(self):
        pc_ifno = info.pointcloud_info(las_file)
        self.assertAlmostEqual(pc_ifno["x_min"], -8.017, places=2)
        self.assertAlmostEqual(pc_ifno["x_max"], 15.924, places=2)
        self.assertAlmostEqual(pc_ifno["y_min"], -18.85, places=2)
        self.assertAlmostEqual(pc_ifno["y_max"], 1.838, places=2)
        self.assertEqual(pc_ifno["z_min"], 1.0)
        self.assertEqual(pc_ifno["z_max"], 11.0)


if __name__ == "__main__":
    unittest.main()
