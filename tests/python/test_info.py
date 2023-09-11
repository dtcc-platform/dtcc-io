import unittest
from dtcc_io import info


las_file = "data/MinimalCase/pointcloud.las"
buildings = "data/MinimalCase/PropertyMap.shp"
roads = "data/road_network/test_road.shp"
dem_raster = "data/test_dem.tif"
img_raster = "data/14040.png"
mesh = "data/cube.stl"


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


class TestRasterInfo(unittest.TestCase):
    def test_raster_dimensions(self):
        raster_info = info.raster_info(dem_raster)
        self.assertEqual(raster_info["width"], 20)
        self.assertEqual(raster_info["height"], 40)

    def test_raster_channels(self):
        raster_info = info.raster_info(img_raster)
        self.assertEqual(raster_info["channels"], 3)
        raster_info = info.raster_info(dem_raster)
        self.assertEqual(raster_info["channels"], 1)

    def test_raster_cell_size(self):
        raster_info = info.raster_info(dem_raster)
        self.assertEqual(raster_info["cell_size"], 2.0)

    def test_raster_bounds(self):
        raster_info = info.raster_info(dem_raster)
        self.assertAlmostEqual(raster_info["x_min"], 0.0, places=2)
        self.assertAlmostEqual(raster_info["x_max"], 40.0, places=2)
        self.assertAlmostEqual(raster_info["y_min"], -80.0, places=2)
        self.assertAlmostEqual(raster_info["y_max"], 0.0, places=2)


class TestMeshInfo(unittest.TestCase):
    def test_mesh_vertices(self):
        info_dict = info.mesh_info(mesh)
        self.assertEqual(info_dict["vertices"], 24)

    def test_mesh_faces(self):
        info_dict = info.mesh_info(mesh)
        self.assertEqual(info_dict["faces"], 44)

    def test_mesh_bounds(self):
        info_dict = info.mesh_info(mesh)
        self.assertAlmostEqual(info_dict["x_min"], -1.0, places=2)
        self.assertAlmostEqual(info_dict["x_max"], 1.0, places=2)
        self.assertAlmostEqual(info_dict["y_min"], -1.0, places=2)
        self.assertAlmostEqual(info_dict["y_max"], 1.0, places=2)
        self.assertAlmostEqual(info_dict["z_min"], -1.0, places=2)
        self.assertAlmostEqual(info_dict["z_max"], 1.0, places=2)


if __name__ == "__main__":
    unittest.main()
