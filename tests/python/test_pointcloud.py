import unittest

from pathlib import Path
import json
import dtcc_io as io
import tempfile

class TestPointcloud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = (Path(__file__).parent / ".." / "data" / "MinimalCase").resolve()
        cls.building_las_file = str(
            (
                cls.data_dir / "pointcloud.las"
            ).resolve()
        )

    def test_load_pointcloud(self):
        pc = io.load_pointcloud(self.building_las_file, return_serialized=False)
        self.assertEqual(len(pc.points), 8148)
        self.assertEqual(len(pc.classification), 8148)
        self.assertEqual(len(pc.usedClassifications), 2)

    def test_load_pointcloud_from_dir(self):
        pc = io.load_pointcloud(self.data_dir, return_serialized=False)
        self.assertEqual(len(pc.points), 8148)

    def test_load_pointcloud_bounded(self):
        pc = io.load_pointcloud(self.building_las_file,  bounds=(-2, -2, 0, 0), return_serialized=False)
        self.assertEqual(len(pc.points), 64)
        self.assertEqual(len(pc.classification), 64)

    def test_point_cloud_bounds(self):
        bounds = io.pointcloud.calc_las_bounds(self.building_las_file)
        self.assertAlmostEqual(bounds[0], -8.01747, places=3)
        self.assertAlmostEqual(bounds[1], -18.850332, places=3)
        self.assertAlmostEqual(bounds[2], 15.92373, places=3)
        self.assertAlmostEqual(bounds[3], 1.83826, places=3)
        
    def test_save_json(self):
        pc = io.load_pointcloud(self.building_las_file, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        outpath = Path(outfile.name)
        io.save_pointcloud(pc, outfile.name)
        with open(outpath, "r") as f:
            json_data = json.load(f)
        self.assertEqual(len(json_data["points"]), 8148)
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()
