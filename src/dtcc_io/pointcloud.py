from pathlib import Path
import numpy as np
import laspy
from time import time

from dtcc_model import dtcc_pb2 as proto
from dtcc_model import PointCloud, Bounds
from .logging import info, warning, error

# from dtcc_io.bindings import PBPointCloud

from . import generic


def las_file_bounds(las_file):
    src = laspy.read(las_file)
    bounds = Bounds(
        src.header.x_min, src.header.y_min, src.header.x_max, src.header.y_max
    )
    return bounds


def calc_las_bounds(las_path):
    las_path = Path(las_path)
    if not las_path.exists():
        raise ValueError(f"Path {las_path} does not exist")
    if las_path.is_file():
        bbox = las_file_bounds(las_path)
    if las_path.is_dir():
        bbox = None
        for f in las_path.glob("*.la[sz]"):
            if bbox is None:
                bbox = las_file_bounds(f)
            else:
                bbox = bbox.union(las_file_bounds(f))
    return bbox


def bounds_filter_poinst(pts, bounds):
    if bounds is not None and len(bounds) == 4:
        valid_pts = (pts[:, 0] >= bounds[0]) * (pts[:, 0] <= bounds[2])  # valid X
        valid_pts *= (pts[:, 1] >= bounds[1]) * (pts[:, 1] <= bounds[3])  # valid Y
    else:
        valid_pts = np.ones(pts.shape[0]).astype(bool)
    return valid_pts


def load(
    path,
    points_only=False,
    points_classification_only=False,
    delimiter=",",
    bounds=(),
):
    path = Path(path)
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")
    info(f"Loading pointcloud from {path}")
    if path.is_dir():
        return load_dir(
            path,
            points_only=points_only,
            points_classification_only=points_classification_only,
            delimiter=delimiter,
            glob="*.la[sz]",
            bounds=bounds,
        )
    else:
        return generic.load(
            path,
            "pointcloud",
            PointCloud,
            _load_formats,
            points_only=points_only,
            points_classification_only=points_classification_only,
            delimiter=delimiter,
            bounds=bounds,
        )


def load_dir(
    path,
    points_only=False,
    points_classification_only=False,
    delimiter=",",
    glob="*.la[sz]",
    bounds=(),
):
    pc = PointCloud()
    for f in path.glob(glob):
        t_pc = load(
            f,
            points_only=points_only,
            points_classification_only=points_classification_only,
            delimiter=delimiter,
            bounds=bounds,
        )
        if t_pc is not None:
            pc.merge(t_pc)
    return pc


def _load_csv(path, point_only=False, delimiter=",", bounds=(), **kwargs):
    pts = np.loadtxt(path, delimiter=delimiter)
    valid_pts = bounds_filter_poinst(pts, bounds)
    if len(valid_pts) == 0:
        warning(f"Pointcloud {path} has no points")
        return PointCloud()
    if pts.shape[1] < 3:
        error(f"Pointcloud {path} has less than 3 dimensions")
        return None
    pc = PointCloud()
    pc.points = pts[:, :3][valid_pts]
    if not point_only and pts.shape[1] >= 4:
        pc.classification = pts[:, 3][valid_pts].astype(np.uint8)
    pc.calculate_bounds()
    return pc


# def load_dir(
#     las_dir,
#     points_only=False,
#     points_classification_only=False,
#     bounds=(),
# ):
#     las_files = list(las_dir.glob("*.la[sz]"))
#     return load_las(las_files, points_only, points_classification_only, bounds)


def _load_las(
    lasfile: Path,
    points_only=False,
    points_classification_only=False,
    bounds=(),
    **kwargs,
):
    use_bounds_filter = bounds is not None and len(bounds) == 4
    las = laspy.read(lasfile)
    classification = np.array([]).astype(np.uint8)
    intensity = np.array([]).astype(np.uint16)
    returnNumber = np.array([]).astype(np.uint8)
    numberOfReturns = np.array([]).astype(np.uint8)
    pts = np.array(las.xyz)

    if use_bounds_filter:
        valid_pts = bounds_filter_poinst(pts, bounds)
        pts = pts[valid_pts]

    if len(pts) == 0:
        warning(f"Pointcloud {lasfile} has no points")
        return PointCloud()

    if not points_only:
        classification = np.array(las.classification)
        if use_bounds_filter:
            classification = classification[valid_pts]
    if not (points_only or points_classification_only):
        intensity = np.array(las.intensity)
        returnNumber = np.array(las.return_num)
        numberOfReturns = np.array(las.num_returns)
        if use_bounds_filter:
            intensity = intensity[valid_pts]
            returnNumber = returnNumber[valid_pts]
            numberOfReturns = numberOfReturns[valid_pts]
    pc = PointCloud()
    pc.points = pts
    if not points_only:
        pc.classification = classification
    if not (points_only or points_classification_only):
        pc.intensity = intensity
        pc.return_number = returnNumber
        pc.num_returns = numberOfReturns
    pc.calculate_bounds()
    return pc


def _load_proto_pointcloud(path, **kwargs):
    with open(path, "rb") as f:
        return PointCloud.from_proto(f.read())


def save(pointcloud, outfile):
    generic.save(pointcloud, outfile, "pointcloud", _save_formats)


def _save_csv(pointcloud, outfile):
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    np.savetxt(outfile, pts, delimiter=",")


def _save_las(pointcloud, las_file):
    # hdr = laspy.header
    # las = laspy.create(point_format=2, file_version="1.2")

    outfile = laspy.create(point_format=2, file_version="1.2")
    # outfile = laspy.file.File(las_file, mode="w")
    # outfile.header.point_format_id = 2
    outfile.x = pointcloud.points[:, 0]
    outfile.y = pointcloud.points[:, 1]
    outfile.z = pointcloud.points[:, 2]
    if len(pointcloud.classification) == len(pointcloud.points):
        outfile.classification = pointcloud.classification
    outfile.write(las_file)


def _save_proto_pointcloud(pointcloud, outfile):
    outfile = Path(outfile)
    outfile.write_bytes(pointcloud.to_proto().SerializeToString())


def _save_json_pointcloud(pointcloud, outfile):
    outfile = Path(outfile)
    outfile.write_text(pointcloud.to_json())


def list_io():
    return generic.list_io("mesh", _load_formats, _save_formats)


def print_io():
    generic.print_io("mesh", _load_formats, _save_formats)


_load_formats = {
    PointCloud: {
        ".pb": _load_proto_pointcloud,
        ".pb2": _load_proto_pointcloud,
        ".las": _load_las,
        ".laz": _load_las,
        ".csv": _load_csv,
    }
}

_save_formats = {
    PointCloud: {
        ".pb": _save_proto_pointcloud,
        ".pb2": _save_proto_pointcloud,
        ".json": _save_json_pointcloud,
        ".las": _save_las,
        ".laz": _save_las,
        ".csv": _save_csv,
    }
}
