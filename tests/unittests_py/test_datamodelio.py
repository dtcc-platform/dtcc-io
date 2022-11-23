import unittest

import sys
from pathlib import Path

sys.path.append(str((Path(__file__).parent.parent.parent).resolve()))
print(sys.path)
from dtcc.io import PointCloudIO, CityModelIO, MeshIO
import tempfile, os


class TestBuildings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.building_shp_file = str(
            (
                Path(__file__).parent
                / ".."
                / "data"
                / "MinimalCase"
                / "propertyMap.shp"
            ).resolve()
        )
        cls.building_las_file = str(
            (
                Path(__file__).parent / ".." / "data" / "MinimalCase" / "pointcloud.las"
            ).resolve()
        )
        cls.stl_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.stl").resolve()
        )
        cls.fbx_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.fbx").resolve()
        )

    # def test_load_shp_buildings(self):
    #     print("reading shp file")
    #     cm = CityModelIO.read(self.building_shp_file, "uuid")
    #     print("done")
    #     print(len(cm.buildings))
    #     self.assertEqual(len(cm.buildings), 5)
    #     print("reading shp file2")
    #     cm2 = CityModelIO.read(self.building_shp_file, "uuid", area_filter=36)
    #     print("done2")
    #     self.assertEqual(len(cm2.buildings), 4)

    def test_load_pointcloud(self):
        pc = PointCloudIO.read(self.building_las_file, return_serialized=False)
        self.assertEqual(len(pc.points), 8148)
        self.assertEqual(len(pc.classification), 8148)
        self.assertEqual(len(pc.usedClassifications), 2)

    def test_load_meshio_mesh(self):
        mesh = MeshIO.read(self.stl_mesh_cube, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def test_write_meshio_mesh(self):
        mesh = MeshIO.read(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False)
        MeshIO.write(outfile.name, mesh)
        mesh = MeshIO.read(outfile.name, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)
        os.unlink(outfile.name)

    # def test_load_assimp_mesh(self):
    #     mesh = MeshIO.read(self.fbx_mesh_cube,return_serialized=False)
    #     self.assertEqual(len(mesh.vertices), 24)
    #     self.assertEqual(len(mesh.faces), 44)


if __name__ == "__main__":
    unittest.main()
