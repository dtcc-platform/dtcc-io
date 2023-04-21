from pathlib import Path
import numpy as np
import laspy
from time import time
import logging

from dtcc_model import dtcc_pb2 as proto
from dtcc_model import PointCloud

# FIXME: Use Bounds class from dtcc-model
from dtcc_io.bounds import bounds_union

# from dtcc_io.bindings import PBPointCloud

from .utils import protobuf_to_json


def las_file_bounds(las_file):
    src = laspy.read(las_file)
    bounds = (src.header.x_min, src.header.y_min, src.header.x_max, src.header.y_max)
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
                bbox = bounds_union(bbox, las_file_bounds(f))
    return bbox


def load(
    path,
    points_only=False,
    points_classification_only=False,
    delimiter=",",
    bounds=(),
):
    path = Path(path)
    suffix = path.suffix.lower()
    if len(bounds) > 0 and len(bounds) != 4:
        print("WARNING, invalid bouds {bounds}, ignoring")
        bounds = ()
    if path.is_dir():
        return load_dir(
            path,
            points_only=points_only,
            points_classification_only=points_classification_only,
            bounds=bounds,
        )
    if suffix in [".pb", ".pb2"]:
        pc = PointCloud()
        pc.from_proto(path.load_bytes())
        return pc
    elif suffix in [".las", ".laz"]:
        return load_las(
            path,
            points_only=points_only,
            points_classification_only=points_classification_only,
            bounds=bounds,
        )
    elif suffix in [".csv"]:
        return load_csv(
            path,
            delimiter=delimiter,
            bounds=bounds,
        )
    else:
        print(f"Cannot read file with suffix {suffix}")
    return None


def load_csv(path, delimiter=",", bounds=()):
    pass
    pts = np.loadtxt(path, delimiter=delimiter)
    valid_pts = bounds_filter_poinst(pts, bounds)
    assert pts.shape[1] >= 3
    pc = Pointcloud()
    pc.points = pts[:, :3][valid_pts]
    if pts.shape[1] >= 4:
        pc.classification = pts[:, 3][valid_pts].astype(np.uint8)
    return pc


def load_dir(
    las_dir,
    points_only=False,
    points_classification_only=False,
    bounds=(),
):
    las_files = list(las_dir.glob("*.la[sz]"))
    return load_las(las_files, points_only, points_classification_only, bounds)


def bounds_filter_poinst(pts, bounds):
    if bounds is not None and len(bounds) == 4:
        valid_pts = (pts[:, 0] >= bounds[0]) * (pts[:, 0] <= bounds[2])  # valid X
        valid_pts *= (pts[:, 1] >= bounds[1]) * (pts[:, 1] <= bounds[3])  # valid Y
    else:
        valid_pts = np.ones(pts.shape[0]).astype(bool)
    return valid_pts


def load_las(
    lasfiles,
    points_only=False,
    points_classification_only=False,
    bounds=(),
):
    if isinstance(lasfiles, str) or isinstance(lasfiles, Path):
        lasfiles = [lasfiles]
    pts = None
    classification = np.array([]).astype(np.uint8)
    intensity = np.array([]).astype(np.uint16)
    returnNumber = np.array([]).astype(np.uint8)
    numberOfReturns = np.array([]).astype(np.uint8)
    start_laspy = time()
    use_bounds_filter = len(bounds) == 4

    for filename in lasfiles:
        las = laspy.read(filename)
        valid_pts = bounds_filter_poinst(las.xyz, bounds)
        if pts is None:
            pts = las.xyz[valid_pts]
        else:
            pts = np.concatenate((pts, las.xyz[valid_pts]))

        if not points_only:
            classification = np.concatenate(
                (classification, np.array(las.classification)[valid_pts])
            )
        if not (points_only or points_classification_only):
            intensity = np.concatenate((intensity, np.array(las.intensity)[valid_pts]))
            returnNumber = np.concatenate(
                (returnNumber, np.array(las.return_num)[valid_pts])
            )
            numberOfReturns = np.concatenate(
                (numberOfReturns, np.array(las.num_returns)[valid_pts])
            )
    # print(f"loading with laspy {time()-start_laspy}")
    start_protobuf_pc = time()
    if pts is not None and len(pts) > 0:
        pc = Pointcloud()
        pc.points = pts
        if not points_only:
            pc.classification = classification
        if not (points_only or points_classification_only):
            pc.intensity = intensity
            pc.return_number = returnNumber
            pc.number_of_returns = numberOfReturns
        logging.info(f"Loaded {len(pts)} points from {lasfiles}")
        return pc
    else:
        logging.warning(f"Could not load any points from {lasfiles}")
        return None


def save(pointcloud, outfile):
    outfile = Path(outfile)
    suffix = outfile.suffix.lower()
    if suffix in [".las", ".laz"]:
        save_las(pointcloud, outfile)
    elif suffix in [".csv"]:
        save_csv(pointcloud, outfile)
    elif suffix in [".pb", ".pb2"]:
        outfile.write_bytes(pointcloud.to_proto().SerializeToString())
    elif suffix in [".json"]:
        protobuf_to_json(pointcloud, outfile)
    else:
        print(f"Cannot write file with suffix {suffix}")


def save_csv(pointcloud, outfile):
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    np.savetxt(outfile, pts, delimiter=",")


def save_las(pointcloud, las_file):
    # hdr = laspy.header
    # las = laspy.create(point_format=2, file_version="1.2")

    outfile = laspy.create(point_format=2, file_version="1.2")
    # outfile = laspy.file.File(las_file, mode="w")
    # outfile.header.point_format_id = 2
    outfile.x = pointcloud.points[:, 0]
    outfile.y = pointcloud.points[:, 1]
    outfile.z = pointcloud.points[:, 2]
    outfile.classification = pointcloud.classification
    outfile.write(las_file)
