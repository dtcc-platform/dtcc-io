# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dtcc.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndtcc.proto\x12\x04\x44TCC\" \n\x08Vector2D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\"+\n\x08Vector3D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"#\n\tSimplex1D\x12\n\n\x02v0\x18\x01 \x01(\x05\x12\n\n\x02v1\x18\x02 \x01(\x05\"/\n\tSimplex2D\x12\n\n\x02v0\x18\x01 \x01(\x05\x12\n\n\x02v1\x18\x02 \x01(\x05\x12\n\n\x02v2\x18\x03 \x01(\x05\";\n\tSimplex3D\x12\n\n\x02v0\x18\x01 \x01(\x05\x12\n\n\x02v1\x18\x02 \x01(\x05\x12\n\n\x02v2\x18\x03 \x01(\x05\x12\n\n\x02v3\x18\x04 \x01(\x05\"E\n\rBoundingBox2D\x12\x19\n\x01p\x18\x01 \x01(\x0b\x32\x0e.DTCC.Vector2D\x12\x19\n\x01q\x18\x02 \x01(\x0b\x32\x0e.DTCC.Vector2D\"E\n\rBoundingBox3D\x12\x19\n\x01p\x18\x01 \x01(\x0b\x32\x0e.DTCC.Vector3D\x12\x19\n\x01q\x18\x02 \x01(\x0b\x32\x0e.DTCC.Vector3D\",\n\nMultiPoint\x12\x1e\n\x06points\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector2D\".\n\x0cMultiPoint3D\x12\x1e\n\x06points\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector3D\".\n\nLineString\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector2D\"0\n\x0cLineString3D\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector3D\".\n\nLinearRing\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector2D\"K\n\x07Polygon\x12\x1f\n\x05shell\x18\x01 \x01(\x0b\x32\x10.DTCC.LinearRing\x12\x1f\n\x05holes\x18\x02 \x03(\x0b\x32\x10.DTCC.LinearRing\"/\n\x0cMultiPolygon\x12\x1f\n\x08polygons\x18\x01 \x03(\x0b\x32\r.DTCC.Polygon\"n\n\x06Grid2D\x12(\n\x0b\x62oundingBox\x18\x01 \x01(\x0b\x32\x13.DTCC.BoundingBox2D\x12\r\n\x05xSize\x18\x02 \x01(\x05\x12\r\n\x05ySize\x18\x03 \x01(\x05\x12\r\n\x05xStep\x18\x04 \x01(\x02\x12\r\n\x05yStep\x18\x05 \x01(\x02\"\x8c\x01\n\x06Grid3D\x12(\n\x0b\x62oundingBox\x18\x01 \x01(\x0b\x32\x13.DTCC.BoundingBox3D\x12\r\n\x05xSize\x18\x02 \x01(\x05\x12\r\n\x05ySize\x18\x03 \x01(\x05\x12\r\n\x05zSize\x18\x04 \x01(\x05\x12\r\n\x05xStep\x18\x05 \x01(\x02\x12\r\n\x05yStep\x18\x06 \x01(\x02\x12\r\n\x05zStep\x18\x07 \x01(\x02\"[\n\x06Mesh2D\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector2D\x12\x1e\n\x05\x63\x65lls\x18\x02 \x03(\x0b\x32\x0f.DTCC.Simplex2D\x12\x0f\n\x07markers\x18\x03 \x03(\x05\"[\n\x06Mesh3D\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector3D\x12\x1e\n\x05\x63\x65lls\x18\x02 \x03(\x0b\x32\x0f.DTCC.Simplex3D\x12\x0f\n\x07markers\x18\x03 \x03(\x05\"n\n\tSurface2D\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector2D\x12\x1f\n\x07normals\x18\x02 \x03(\x0b\x32\x0e.DTCC.Vector2D\x12\x1e\n\x05\x65\x64ges\x18\x03 \x03(\x0b\x32\x0f.DTCC.Simplex1D\"n\n\tSurface3D\x12 \n\x08vertices\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector3D\x12\x1f\n\x07normals\x18\x02 \x03(\x0b\x32\x0e.DTCC.Vector3D\x12\x1e\n\x05\x66\x61\x63\x65s\x18\x03 \x03(\x0b\x32\x0f.DTCC.Simplex2D\"9\n\x0bGridField2D\x12\x1a\n\x04grid\x18\x01 \x01(\x0b\x32\x0c.DTCC.Grid2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"9\n\x0bGridField3D\x12\x1a\n\x04grid\x18\x01 \x01(\x0b\x32\x0c.DTCC.Grid3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"?\n\x11GridVectorField2D\x12\x1a\n\x04grid\x18\x01 \x01(\x0b\x32\x0c.DTCC.Grid2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"?\n\x11GridVectorField3D\x12\x1a\n\x04grid\x18\x01 \x01(\x0b\x32\x0c.DTCC.Grid3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"9\n\x0bMeshField2D\x12\x1a\n\x04mesh\x18\x01 \x01(\x0b\x32\x0c.DTCC.Mesh2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"9\n\x0bMeshField3D\x12\x1a\n\x04mesh\x18\x01 \x01(\x0b\x32\x0c.DTCC.Mesh3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"?\n\x11MeshVectorField2D\x12\x1a\n\x04mesh\x18\x01 \x01(\x0b\x32\x0c.DTCC.Mesh2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"?\n\x11MeshVectorField3D\x12\x1a\n\x04mesh\x18\x01 \x01(\x0b\x32\x0c.DTCC.Mesh3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"B\n\x0eSurfaceField2D\x12 \n\x07surface\x18\x01 \x01(\x0b\x32\x0f.DTCC.Surface2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"B\n\x0eSurfaceField3D\x12 \n\x07surface\x18\x01 \x01(\x0b\x32\x0f.DTCC.Surface3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"H\n\x14SurfaceVectorField2D\x12 \n\x07surface\x18\x01 \x01(\x0b\x32\x0f.DTCC.Surface2D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"H\n\x14SurfaceVectorField3D\x12 \n\x07surface\x18\x01 \x01(\x0b\x32\x0f.DTCC.Surface3D\x12\x0e\n\x06values\x18\x02 \x03(\x02\"\xed\x01\n\nPointCloud\x12\x1e\n\x06points\x18\x01 \x03(\x0b\x32\x0e.DTCC.Vector3D\x12#\n\x06\x62ounds\x18\x02 \x01(\x0b\x32\x13.DTCC.BoundingBox2D\x12\x16\n\x0e\x63lassification\x18\x03 \x03(\r\x12\x11\n\tintensity\x18\x04 \x03(\r\x12\x14\n\x0creturnNumber\x18\x05 \x03(\r\x12\x12\n\nnumReturns\x18\x06 \x03(\r\x12\x1b\n\x13usedClassifications\x18\x07 \x03(\r\x12(\n\x0cgeoreference\x18\x08 \x01(\x0b\x32\x12.DTCC.Georeference\"\x95\x01\n\x08\x42uilding\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12 \n\tfootPrint\x18\x02 \x01(\x0b\x32\r.DTCC.Polygon\x12\x0e\n\x06height\x18\x03 \x01(\x01\x12\x14\n\x0cgroundHeight\x18\x04 \x01(\x01\x12$\n\nroofpoints\x18\x05 \x01(\x0b\x32\x10.DTCC.PointCloud\x12\r\n\x05\x65rror\x18\x06 \x01(\x04\"X\n\tCityModel\x12!\n\tbuildings\x18\x01 \x03(\x0b\x32\x0e.DTCC.Building\x12(\n\x0cgeoreference\x18\x03 \x01(\x0b\x32\x12.DTCC.Georeference\"A\n\x0cGeoreference\x12\x0b\n\x03\x63rs\x18\x01 \x01(\t\x12\x0c\n\x04\x65psg\x18\x02 \x01(\x05\x12\n\n\x02x0\x18\x03 \x01(\x01\x12\n\n\x02y0\x18\x04 \x01(\x01\x42\x02H\x03\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dtcc_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\003'
  _VECTOR2D._serialized_start=20
  _VECTOR2D._serialized_end=52
  _VECTOR3D._serialized_start=54
  _VECTOR3D._serialized_end=97
  _SIMPLEX1D._serialized_start=99
  _SIMPLEX1D._serialized_end=134
  _SIMPLEX2D._serialized_start=136
  _SIMPLEX2D._serialized_end=183
  _SIMPLEX3D._serialized_start=185
  _SIMPLEX3D._serialized_end=244
  _BOUNDINGBOX2D._serialized_start=246
  _BOUNDINGBOX2D._serialized_end=315
  _BOUNDINGBOX3D._serialized_start=317
  _BOUNDINGBOX3D._serialized_end=386
  _MULTIPOINT._serialized_start=388
  _MULTIPOINT._serialized_end=432
  _MULTIPOINT3D._serialized_start=434
  _MULTIPOINT3D._serialized_end=480
  _LINESTRING._serialized_start=482
  _LINESTRING._serialized_end=528
  _LINESTRING3D._serialized_start=530
  _LINESTRING3D._serialized_end=578
  _LINEARRING._serialized_start=580
  _LINEARRING._serialized_end=626
  _POLYGON._serialized_start=628
  _POLYGON._serialized_end=703
  _MULTIPOLYGON._serialized_start=705
  _MULTIPOLYGON._serialized_end=752
  _GRID2D._serialized_start=754
  _GRID2D._serialized_end=864
  _GRID3D._serialized_start=867
  _GRID3D._serialized_end=1007
  _MESH2D._serialized_start=1009
  _MESH2D._serialized_end=1100
  _MESH3D._serialized_start=1102
  _MESH3D._serialized_end=1193
  _SURFACE2D._serialized_start=1195
  _SURFACE2D._serialized_end=1305
  _SURFACE3D._serialized_start=1307
  _SURFACE3D._serialized_end=1417
  _GRIDFIELD2D._serialized_start=1419
  _GRIDFIELD2D._serialized_end=1476
  _GRIDFIELD3D._serialized_start=1478
  _GRIDFIELD3D._serialized_end=1535
  _GRIDVECTORFIELD2D._serialized_start=1537
  _GRIDVECTORFIELD2D._serialized_end=1600
  _GRIDVECTORFIELD3D._serialized_start=1602
  _GRIDVECTORFIELD3D._serialized_end=1665
  _MESHFIELD2D._serialized_start=1667
  _MESHFIELD2D._serialized_end=1724
  _MESHFIELD3D._serialized_start=1726
  _MESHFIELD3D._serialized_end=1783
  _MESHVECTORFIELD2D._serialized_start=1785
  _MESHVECTORFIELD2D._serialized_end=1848
  _MESHVECTORFIELD3D._serialized_start=1850
  _MESHVECTORFIELD3D._serialized_end=1913
  _SURFACEFIELD2D._serialized_start=1915
  _SURFACEFIELD2D._serialized_end=1981
  _SURFACEFIELD3D._serialized_start=1983
  _SURFACEFIELD3D._serialized_end=2049
  _SURFACEVECTORFIELD2D._serialized_start=2051
  _SURFACEVECTORFIELD2D._serialized_end=2123
  _SURFACEVECTORFIELD3D._serialized_start=2125
  _SURFACEVECTORFIELD3D._serialized_end=2197
  _POINTCLOUD._serialized_start=2200
  _POINTCLOUD._serialized_end=2437
  _BUILDING._serialized_start=2440
  _BUILDING._serialized_end=2589
  _CITYMODEL._serialized_start=2591
  _CITYMODEL._serialized_end=2679
  _GEOREFERENCE._serialized_start=2681
  _GEOREFERENCE._serialized_end=2746
# @@protoc_insertion_point(module_scope)
