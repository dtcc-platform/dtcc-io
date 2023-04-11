# Usage
```python
import dtcc_io as io
foo = io.load_foo("my_data.foo")
foo = io.load_foo("my_data.pb")
io.save_foo(foo, "my_data.foo")
```

dtcc_io handles loading and saving both our protobuf messages as well as popular file formats to an from our data models.

we currently have the following function:

- `[load|save]_mesh` supports obj, stl, vtu, gltf2, glb
- `[load|save]_volumemesh` support vtk, vtu
- `[load|save]_pointcloud` supports las, laz, csv
- `[load|save]_citymodel` supports shp,geojson,gpkg
- `[load|save]_elevationmodel` supoprts tif

