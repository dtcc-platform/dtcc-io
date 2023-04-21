import unittest

import json
from pathlib import Path

import os, tempfile
import dtcc_io as io


class TestMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stl_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.stl").resolve()
        )
        cls.fbx_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.fbx").resolve()
        )

    def test_load_mesh_stl(self):
        mesh = io.load_mesh(self.stl_mesh_cube)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def _test_write_meshio_mesh(self):
        mesh = io.load_mesh(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False)
        outpath = Path(outfile.name)
        io.save_mesh(mesh, outfile.name)
        mesh = io.load_mesh(outpath, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)
        outfile.close()
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

    def _test_write_to_json(self):
        mesh = io.load_mesh(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        outpath = Path(outfile.name)
        io.save_mesh(mesh, outpath)
        with open(outpath, "r") as f:
            json_data = json.load(f)
        self.assertEqual(len(json_data["vertices"]), 24)
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

    def _test_write_gltf(self):
        mesh = io.load_mesh(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".gltf", delete=False)
        outpath = Path(outfile.name)
        # outpath = Path("test_cube.gltf")
        io.save_mesh(mesh, outpath)
        # mesh = io.load_mesh(outpath, return_serialized=False)
        # self.assertEqual(len(mesh.vertices), 24)
        # self.assertEqual(len(mesh.faces), 44)
        outfile.close()
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

    def _test_write_glb(self):
        mesh = io.load_mesh(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".glb", delete=False)
        outpath = Path(outfile.name)
        io.save_mesh(mesh, outpath)
        # mesh = io.load_mesh(outpath, return_serialized=False)
        # self.assertEqual(len(mesh.vertices), 24)
        # self.assertEqual(len(mesh.faces), 44)
        outfile.close()
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
