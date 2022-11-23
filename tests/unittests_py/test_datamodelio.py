import unittest

import sys
from pathlib import Path

sys.path.append(str((Path(__file__).parent.parent.parent).resolve()))
from dtcc.io import PointCloudIO, CityModelIO, MeshIO, ElevationModelIO
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

        cls.dem_raster = str(
            (Path(__file__).parent / ".." / "data" / "testraster.tif").resolve()
        )

    def test_load_shp_buildings(self):
        cm = CityModelIO.read(self.building_shp_file, "uuid")
        self.assertEqual(len(cm.buildings), 5)
        cm2 = CityModelIO.read(self.building_shp_file, "uuid", area_filter=36)
        self.assertEqual(len(cm2.buildings), 4)

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

    def test_load_assimp_mesh(self):
        mesh = MeshIO.read(self.fbx_mesh_cube, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 132)
        self.assertEqual(len(mesh.faces), 44)

    # def test_write_assimp_mesh(self):
    #     mesh = MeshIO.read(self.fbx_mesh_cube, return_serialized=False)
    #     outfile = tempfile.NamedTemporaryFile(suffix=".fbx", delete=False)
    #     MeshIO.write(outfile.name, mesh)
    #     mesh = MeshIO.read(outfile.name, return_serialized=False)
    #     self.assertEqual(len(mesh.vertices), 24)
    #     self.assertEqual(len(mesh.faces), 44)
    #     os.unlink(outfile.name)

    def test_load_elevation_model(self):
        em = ElevationModelIO.read(self.dem_raster, return_serialized=False)
        self.assertEqual(em.grid.xStep, 0.5)

    def test_write_elevation_model(self):
        em = ElevationModelIO.read(self.dem_raster, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".tif", delete=False).name
        ElevationModelIO.write(outfile, em)
        em = ElevationModelIO.read(outfile, return_serialized=False)
        self.assertEqual(em.grid.xStep, 0.5)
        os.unlink(outfile)

if __name__ == "__main__":
    unittest.main()
