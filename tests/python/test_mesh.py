import unittest
import json
import os, tempfile, pathlib
import dtcc_io as io
from dtcc_model import Mesh, VolumeMesh
import numpy as np


class TestMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mesh_cube_stl = str(
            (pathlib.Path(__file__).parent / ".." / "data" / "cube.stl").resolve()
        )
        cls.mesh_cube_vtk = str(
            (pathlib.Path(__file__).parent / ".." / "data" / "cube.vtk").resolve()
        )
        cls.mesh_cube_fbx = str(
            (pathlib.Path(__file__).parent / ".." / "data" / "cube.fbx").resolve()
        )

    # FIXME: Not really testing all formats here, just a few

    def test_load_mesh_stl(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def test_load_mesh_vtk(self):
        mesh = io.load_mesh(self.mesh_cube_vtk)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    # FIXME: This segfaults
    def _test_load_mesh_fbx(self):
        mesh = io.load_mesh(self.mesh_cube_fbx)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def test_save_load_mesh_stl(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        path = tempfile.NamedTemporaryFile(suffix=".stl", delete=False).name
        io.save_mesh(mesh, path)
        mesh = io.load_mesh(path)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def test_save_load_mesh_vtk(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        path = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False).name
        io.save_mesh(mesh, path)
        mesh = io.load_mesh(path)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    # FIXME: Save to FBX not implemented
    def _test_save_load_mesh_fbx(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        path = tempfile.NamedTemporaryFile(suffix=".fbx", delete=False).name
        io.save_mesh(mesh, path)
        mesh = io.load_mesh(path)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    # FIXME: Load from GLB not implemented
    def test_save_load_mesh_glb(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        path = tempfile.NamedTemporaryFile(suffix=".glb", delete=False).name
        mesh.save(path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)
        # mesh = io.load_mesh(path)
        # self.assertEqual(len(mesh.vertices), 24)
        # self.assertEqual(len(mesh.faces), 44)

    # FIXME: Load from GLTF not implemented
    def test_save_load_mesh_gltf(self):
        mesh = io.load_mesh(self.mesh_cube_stl)
        path = tempfile.NamedTemporaryFile(suffix=".gltf", delete=False).name
        mesh.save(path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)
        # mesh = io.load_mesh(path)
        # self.assertEqual(len(mesh.vertices), 24)
        # self.assertEqual(len(mesh.faces), 44)


class TestVolumeMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        verts = vertices = np.array(
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 1],
                [1, 1, 1],
                [0, 1, 1],
            ]
        )
        cells = np.array(
            [
                [0, 1, 2, 4],
                [1, 2, 3, 5],
                [2, 3, 0, 6],
                [3, 0, 1, 7],
                [0, 4, 5, 1],
                [2, 6, 7, 3],
            ]
        )
        cls.volume_mesh_cube = VolumeMesh(vertices=verts, cells=cells)

    def test_write_read_volume_mesh(self):
        path = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False).name
        self.volume_mesh_cube.save(path)
        self.assertTrue(os.path.exists(path))
        mesh = io.load_volume_mesh(path)
        self.assertEqual(len(mesh.vertices), 8)
        self.assertEqual(len(mesh.cells), 6)
        self.assertTrue(mesh.cells.dtype == np.int64)
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
