import unittest
from dtcc_io import info


las_file = "data/MinimalCase/pointcloud.las"
buildings = "data/MinimalCase/PropertyMap.shp"
roads = "data/road_network/test_road.shp"


class TestPointcloudInfo(unittest.TestCase):
    def test_point_count(self):
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


class TestVectorInfo(unittest.TestCase):
    def test_feature_count(self):
        feature_info = info.vector_info(buildings)
        self.assertEqual(feature_info["count"], 3)

    def test_bounds(self):
        feature_info = info.vector_info(buildings)
        self.assertAlmostEqual(feature_info["x_min"], -5.142, places=2)
        self.assertAlmostEqual(feature_info["x_max"], 12.99, places=2)
        self.assertAlmostEqual(feature_info["y_min"], -15.975, places=2)
        self.assertAlmostEqual(feature_info["y_max"], -1.098, places=2)

    def test_geometry_type_polygon(self):
        feature_info = info.vector_info(buildings)
        self.assertEqual(feature_info["geometry_type"], "Polygon")

    def test_geometry_type_line(self):
        feature_info = info.vector_info(roads)
        self.assertEqual(feature_info["geometry_type"], "LineString")


if __name__ == "__main__":
    unittest.main()
