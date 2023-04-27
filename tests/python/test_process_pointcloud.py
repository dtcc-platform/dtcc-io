import unittest

import dtcc_io as io
from dtcc_model import PointCloud


class TestRemoveGlobalOutliers(unittest.TestCase):
    def test_remove_nothing(self):
        pc = io.load_pointcloud("data/MinimalCase/pointcloud.las")
        pc = pc.remove_global_outliers(1000)
        self.assertEqual(len(pc.points), 8148)

    def test_remove_all(self):
        pc = io.load_pointcloud("data/MinimalCase/pointcloud.las")
        pc = pc.remove_global_outliers(0)
        self.assertEqual(len(pc.points), 0)

    def test_remove_some(self):
        pc = io.load_pointcloud("data/MinimalCase/pointcloud.las")
        pc = pc.remove_global_outliers(1)
        self.assertEqual(len(pc.points), 6965)
