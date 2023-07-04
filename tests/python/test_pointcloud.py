import unittest

from pathlib import Path
import json
import dtcc_io as io
import tempfile


class TestPointcloud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = (Path(__file__).parent / ".." / "data" / "MinimalCase").resolve()
        cls.building_las_file = str((cls.data_dir / "pointcloud.las").resolve())

    def test_load_pointcloud(self):
        pc = io.load_pointcloud(self.building_las_file)
        self.assertEqual(len(pc.points), 8148)
        self.assertEqual(len(pc.classification), 8148)
        self.assertEqual(len(pc.used_classifications()), 2)

    # def test_load_pointcloud_from_dir(self):
    #     pc = io.load_pointcloud(self.data_dir)
    #     self.assertEqual(len(pc.points), 8148)

    def test_load_pointcloud_bounded(self):
        pc = io.load_pointcloud(self.building_las_file, bounds=(-2, -2, 0, 0))
        self.assertEqual(len(pc.points), 64)
        self.assertEqual(len(pc.classification), 64)

    def test_point_cloud_bounds(self):
        bounds = io.pointcloud.calc_las_bounds(self.building_las_file)
        self.assertAlmostEqual(bounds.xmin, -8.01747, places=3)
        self.assertAlmostEqual(bounds.ymin, -18.850332, places=3)
        self.assertAlmostEqual(bounds.xmax, 15.92373, places=3)
        self.assertAlmostEqual(bounds.ymax, 1.83826, places=3)

    def test_save_pointcloud(self):
        pc = io.load_pointcloud(self.building_las_file)
        outfile = tempfile.NamedTemporaryFile(suffix=".las", delete=False)
        outpath = Path(outfile.name)
        pc.save(outpath)
        pc2 = io.load_pointcloud(outpath)
        self.assertEqual(len(pc.points), len(pc2.points))
        self.assertEqual(len(pc.classification), len(pc2.classification))
        outfile.close()
        outpath.unlink()


if __name__ == "__main__":
    unittest.main()
