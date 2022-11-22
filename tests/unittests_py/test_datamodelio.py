import unittest

import sys
from pathlib import Path

sys.path.append( str((Path(__file__).parent )))
from dtcc.io import PointCloudIO, CityModelIO


class TestBuildings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.building_shp_file = str((Path(__file__).parent / ".."/ "data" / "MinimalCase" / "propertyMap.shp").resolve())
        cls.building_las_file = str((Path(__file__).parent / ".."/ "data" / "MinimalCase" / "pointcloud.las").resolve())

    def test_load_shp_buildings(self):
        cm = CityModel.loadBuildings(self.building_shp_file,'uuid')
        self.assertEqual(len(cm.buildings),5)
        cm2 = CityModel.loadBuildings(self.building_shp_file,'uuid',area_filter = 36)
        self.assertEqual(len(cm2.buildings),4)

    def test_load_pointcloud(self):
        pc = PointCloud.loadLAS(self.building_las_file, return_serialized = False)
        self.assertEqual(len(pc.points),8148)
        self.assertEqual(len(pc.classification),8148)
        self.assertEqual(len(pc.usedClassifications),2)


if __name__ == '__main__':
    unittest.main()