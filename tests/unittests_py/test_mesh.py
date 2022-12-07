import unittest

from pathlib import Path

import os, tempfile
from dtcc import io

class TestMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stl_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.stl").resolve()
        )
        cls.fbx_mesh_cube = str(
            (Path(__file__).parent / ".." / "data" / "cube.fbx").resolve()
        )
    
    def test_load_meshio_mesh(self):
        mesh = io.mesh.read(self.stl_mesh_cube, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)

    def test_write_meshio_mesh(self):
        mesh = io.mesh.read(self.stl_mesh_cube, return_serialized=False)
        outfile = tempfile.NamedTemporaryFile(suffix=".vtk", delete=False)
        outpath = Path(outfile.name)
        io.mesh.write(outpath, mesh)
        mesh = io.mesh.read(outpath, return_serialized=False)
        self.assertEqual(len(mesh.vertices), 24)
        self.assertEqual(len(mesh.faces), 44)
        outfile.close()
        outpath_dir = outpath.parent
        outpath.unlink()
        try:
            outpath_dir.rmdir()
        except OSError:
            pass

if __name__ == "__main__":
    unittest.main()