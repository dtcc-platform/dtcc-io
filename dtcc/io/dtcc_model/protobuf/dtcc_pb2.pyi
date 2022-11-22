from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox2D(_message.Message):
    __slots__ = ["p", "q"]
    P_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    p: Vector2D
    q: Vector2D
    def __init__(self, p: _Optional[_Union[Vector2D, _Mapping]] = ..., q: _Optional[_Union[Vector2D, _Mapping]] = ...) -> None: ...

class BoundingBox3D(_message.Message):
    __slots__ = ["p", "q"]
    P_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    p: Vector3D
    q: Vector3D
    def __init__(self, p: _Optional[_Union[Vector3D, _Mapping]] = ..., q: _Optional[_Union[Vector3D, _Mapping]] = ...) -> None: ...

class Building(_message.Message):
    __slots__ = ["error", "footPrint", "groundHeight", "height", "roofpoints", "uuid"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    GROUNDHEIGHT_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROOFPOINTS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    error: int
    footPrint: Polygon
    groundHeight: float
    height: float
    roofpoints: PointCloud
    uuid: str
    def __init__(self, uuid: _Optional[str] = ..., footPrint: _Optional[_Union[Polygon, _Mapping]] = ..., height: _Optional[float] = ..., groundHeight: _Optional[float] = ..., roofpoints: _Optional[_Union[PointCloud, _Mapping]] = ..., error: _Optional[int] = ...) -> None: ...

class CityModel(_message.Message):
    __slots__ = ["buildings", "georeference"]
    BUILDINGS_FIELD_NUMBER: _ClassVar[int]
    GEOREFERENCE_FIELD_NUMBER: _ClassVar[int]
    buildings: _containers.RepeatedCompositeFieldContainer[Building]
    georeference: Georeference
    def __init__(self, buildings: _Optional[_Iterable[_Union[Building, _Mapping]]] = ..., georeference: _Optional[_Union[Georeference, _Mapping]] = ...) -> None: ...

class Georeference(_message.Message):
    __slots__ = ["crs", "epsg", "x0", "y0"]
    CRS_FIELD_NUMBER: _ClassVar[int]
    EPSG_FIELD_NUMBER: _ClassVar[int]
    X0_FIELD_NUMBER: _ClassVar[int]
    Y0_FIELD_NUMBER: _ClassVar[int]
    crs: str
    epsg: int
    x0: float
    y0: float
    def __init__(self, crs: _Optional[str] = ..., epsg: _Optional[int] = ..., x0: _Optional[float] = ..., y0: _Optional[float] = ...) -> None: ...

class Grid2D(_message.Message):
    __slots__ = ["boundingBox", "xSize", "xStep", "ySize", "yStep"]
    BOUNDINGBOX_FIELD_NUMBER: _ClassVar[int]
    XSIZE_FIELD_NUMBER: _ClassVar[int]
    XSTEP_FIELD_NUMBER: _ClassVar[int]
    YSIZE_FIELD_NUMBER: _ClassVar[int]
    YSTEP_FIELD_NUMBER: _ClassVar[int]
    boundingBox: BoundingBox2D
    xSize: int
    xStep: float
    ySize: int
    yStep: float
    def __init__(self, boundingBox: _Optional[_Union[BoundingBox2D, _Mapping]] = ..., xSize: _Optional[int] = ..., ySize: _Optional[int] = ..., xStep: _Optional[float] = ..., yStep: _Optional[float] = ...) -> None: ...

class Grid3D(_message.Message):
    __slots__ = ["boundingBox", "xSize", "xStep", "ySize", "yStep", "zSize", "zStep"]
    BOUNDINGBOX_FIELD_NUMBER: _ClassVar[int]
    XSIZE_FIELD_NUMBER: _ClassVar[int]
    XSTEP_FIELD_NUMBER: _ClassVar[int]
    YSIZE_FIELD_NUMBER: _ClassVar[int]
    YSTEP_FIELD_NUMBER: _ClassVar[int]
    ZSIZE_FIELD_NUMBER: _ClassVar[int]
    ZSTEP_FIELD_NUMBER: _ClassVar[int]
    boundingBox: BoundingBox3D
    xSize: int
    xStep: float
    ySize: int
    yStep: float
    zSize: int
    zStep: float
    def __init__(self, boundingBox: _Optional[_Union[BoundingBox3D, _Mapping]] = ..., xSize: _Optional[int] = ..., ySize: _Optional[int] = ..., zSize: _Optional[int] = ..., xStep: _Optional[float] = ..., yStep: _Optional[float] = ..., zStep: _Optional[float] = ...) -> None: ...

class GridField2D(_message.Message):
    __slots__ = ["grid", "values"]
    GRID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    grid: Grid2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, grid: _Optional[_Union[Grid2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class GridField3D(_message.Message):
    __slots__ = ["grid", "values"]
    GRID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    grid: Grid3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, grid: _Optional[_Union[Grid3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class GridVectorField2D(_message.Message):
    __slots__ = ["grid", "values"]
    GRID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    grid: Grid2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, grid: _Optional[_Union[Grid2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class GridVectorField3D(_message.Message):
    __slots__ = ["grid", "values"]
    GRID_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    grid: Grid3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, grid: _Optional[_Union[Grid3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class LineString(_message.Message):
    __slots__ = ["vertices"]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector2D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ...) -> None: ...

class LineString3D(_message.Message):
    __slots__ = ["vertices"]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector3D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ...) -> None: ...

class LinearRing(_message.Message):
    __slots__ = ["vertices"]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector2D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ...) -> None: ...

class Mesh2D(_message.Message):
    __slots__ = ["cells", "markers", "vertices"]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedCompositeFieldContainer[Simplex2D]
    markers: _containers.RepeatedScalarFieldContainer[int]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector2D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ..., cells: _Optional[_Iterable[_Union[Simplex2D, _Mapping]]] = ..., markers: _Optional[_Iterable[int]] = ...) -> None: ...

class Mesh3D(_message.Message):
    __slots__ = ["cells", "markers", "vertices"]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedCompositeFieldContainer[Simplex3D]
    markers: _containers.RepeatedScalarFieldContainer[int]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector3D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ..., cells: _Optional[_Iterable[_Union[Simplex3D, _Mapping]]] = ..., markers: _Optional[_Iterable[int]] = ...) -> None: ...

class MeshField2D(_message.Message):
    __slots__ = ["mesh", "values"]
    MESH_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    mesh: Mesh2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, mesh: _Optional[_Union[Mesh2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class MeshField3D(_message.Message):
    __slots__ = ["mesh", "values"]
    MESH_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    mesh: Mesh3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, mesh: _Optional[_Union[Mesh3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class MeshVectorField2D(_message.Message):
    __slots__ = ["mesh", "values"]
    MESH_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    mesh: Mesh2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, mesh: _Optional[_Union[Mesh2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class MeshVectorField3D(_message.Message):
    __slots__ = ["mesh", "values"]
    MESH_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    mesh: Mesh3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, mesh: _Optional[_Union[Mesh3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class MultiPoint(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Vector2D]
    def __init__(self, points: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ...) -> None: ...

class MultiPoint3D(_message.Message):
    __slots__ = ["points"]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Vector3D]
    def __init__(self, points: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ...) -> None: ...

class MultiPolygon(_message.Message):
    __slots__ = ["polygons"]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    polygons: _containers.RepeatedCompositeFieldContainer[Polygon]
    def __init__(self, polygons: _Optional[_Iterable[_Union[Polygon, _Mapping]]] = ...) -> None: ...

class PointCloud(_message.Message):
    __slots__ = ["bounds", "classification", "georeference", "intensity", "numReturns", "points", "returnNumber", "usedClassifications"]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    GEOREFERENCE_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FIELD_NUMBER: _ClassVar[int]
    NUMRETURNS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    RETURNNUMBER_FIELD_NUMBER: _ClassVar[int]
    USEDCLASSIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    bounds: BoundingBox2D
    classification: _containers.RepeatedScalarFieldContainer[int]
    georeference: Georeference
    intensity: _containers.RepeatedScalarFieldContainer[int]
    numReturns: _containers.RepeatedScalarFieldContainer[int]
    points: _containers.RepeatedCompositeFieldContainer[Vector3D]
    returnNumber: _containers.RepeatedScalarFieldContainer[int]
    usedClassifications: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, points: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ..., bounds: _Optional[_Union[BoundingBox2D, _Mapping]] = ..., classification: _Optional[_Iterable[int]] = ..., intensity: _Optional[_Iterable[int]] = ..., returnNumber: _Optional[_Iterable[int]] = ..., numReturns: _Optional[_Iterable[int]] = ..., usedClassifications: _Optional[_Iterable[int]] = ..., georeference: _Optional[_Union[Georeference, _Mapping]] = ...) -> None: ...

class Polygon(_message.Message):
    __slots__ = ["holes", "shell"]
    HOLES_FIELD_NUMBER: _ClassVar[int]
    SHELL_FIELD_NUMBER: _ClassVar[int]
    holes: _containers.RepeatedCompositeFieldContainer[LinearRing]
    shell: LinearRing
    def __init__(self, shell: _Optional[_Union[LinearRing, _Mapping]] = ..., holes: _Optional[_Iterable[_Union[LinearRing, _Mapping]]] = ...) -> None: ...

class Simplex1D(_message.Message):
    __slots__ = ["v0", "v1"]
    V0_FIELD_NUMBER: _ClassVar[int]
    V1_FIELD_NUMBER: _ClassVar[int]
    v0: int
    v1: int
    def __init__(self, v0: _Optional[int] = ..., v1: _Optional[int] = ...) -> None: ...

class Simplex2D(_message.Message):
    __slots__ = ["v0", "v1", "v2"]
    V0_FIELD_NUMBER: _ClassVar[int]
    V1_FIELD_NUMBER: _ClassVar[int]
    V2_FIELD_NUMBER: _ClassVar[int]
    v0: int
    v1: int
    v2: int
    def __init__(self, v0: _Optional[int] = ..., v1: _Optional[int] = ..., v2: _Optional[int] = ...) -> None: ...

class Simplex3D(_message.Message):
    __slots__ = ["v0", "v1", "v2", "v3"]
    V0_FIELD_NUMBER: _ClassVar[int]
    V1_FIELD_NUMBER: _ClassVar[int]
    V2_FIELD_NUMBER: _ClassVar[int]
    V3_FIELD_NUMBER: _ClassVar[int]
    v0: int
    v1: int
    v2: int
    v3: int
    def __init__(self, v0: _Optional[int] = ..., v1: _Optional[int] = ..., v2: _Optional[int] = ..., v3: _Optional[int] = ...) -> None: ...

class Surface2D(_message.Message):
    __slots__ = ["edges", "normals", "vertices"]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    NORMALS_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    edges: _containers.RepeatedCompositeFieldContainer[Simplex1D]
    normals: _containers.RepeatedCompositeFieldContainer[Vector2D]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector2D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ..., normals: _Optional[_Iterable[_Union[Vector2D, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[Simplex1D, _Mapping]]] = ...) -> None: ...

class Surface3D(_message.Message):
    __slots__ = ["faces", "normals", "vertices"]
    FACES_FIELD_NUMBER: _ClassVar[int]
    NORMALS_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    faces: _containers.RepeatedCompositeFieldContainer[Simplex2D]
    normals: _containers.RepeatedCompositeFieldContainer[Vector3D]
    vertices: _containers.RepeatedCompositeFieldContainer[Vector3D]
    def __init__(self, vertices: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ..., normals: _Optional[_Iterable[_Union[Vector3D, _Mapping]]] = ..., faces: _Optional[_Iterable[_Union[Simplex2D, _Mapping]]] = ...) -> None: ...

class SurfaceField2D(_message.Message):
    __slots__ = ["surface", "values"]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    surface: Surface2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, surface: _Optional[_Union[Surface2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class SurfaceField3D(_message.Message):
    __slots__ = ["surface", "values"]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    surface: Surface3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, surface: _Optional[_Union[Surface3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class SurfaceVectorField2D(_message.Message):
    __slots__ = ["surface", "values"]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    surface: Surface2D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, surface: _Optional[_Union[Surface2D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class SurfaceVectorField3D(_message.Message):
    __slots__ = ["surface", "values"]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    surface: Surface3D
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, surface: _Optional[_Union[Surface3D, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ...) -> None: ...

class Vector2D(_message.Message):
    __slots__ = ["x", "y"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Vector3D(_message.Message):
    __slots__ = ["x", "y", "z"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...
