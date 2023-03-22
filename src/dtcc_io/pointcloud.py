from pathlib import Path
import numpy as np
import laspy
from time import time

from dtcc_model import PointCloud
from dtcc_io.bounds import bounds_union
from dtcc_io.bindings import PBPointCloud

def las_file_bounds(las_file):
    src = laspy.read(las_file)
    bounds = (src.header.x_min, src.header.y_min,
              src.header.x_max, src.header.y_max)
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
    return_serialized=False,
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
            return_serialized=return_serialized,
        )
    if suffix in [".pb", ".pb2"]:
        pc = PointCloud()
        pc.ParseFromString(path.load_bytes())
        return pc
    elif suffix in [".las", ".laz"]:
        return load_las(
            path,
            points_only=points_only,
            points_classification_only=points_classification_only,
            bounds=bounds,
            return_serialized=return_serialized,
        )
    elif suffix in [".csv"]:
        return load_csv(
            path,
            delimiter=delimiter,
            bounds=bounds,
            return_serialized=return_serialized,
        )
    else:
        print(f"Cannot read file with suffix {suffix}")
    return None


def load_csv(path, delimiter=",", bounds=(), return_serialized=False):
    pass
    pts = np.loadtxt(path, delimiter=delimiter)
    assert pts.shape[1] >= 3
    pb = PBPointCloud(pts[:, :3])
    if return_serialized:
        return pb
    else:
        pc = PointCloud()
        pc.ParseFromString(pb)
        return pc


def load_dir(
    las_dir,
    points_only=False,
    points_classification_only=False,
    bounds=(),
    return_serialized=False,
):
    las_files = list(las_dir.glob("*.la[sz]"))
    return load_las(
        las_files, points_only, points_classification_only, bounds, return_serialized
    )


def load_las(
    lasfiles,
    points_only=False,
    points_classification_only=False,
    bounds=(),
    return_serialized=False,
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
        if use_bounds_filter:
            valid_pts = (las.xyz[:, 0] >= bounds[0]) * \
                (las.xyz[:, 0] <= bounds[2])  # valid X
            valid_pts *= (las.xyz[:, 1] >= bounds[1]) * \
                (las.xyz[:, 1] <= bounds[3])  # valid Y
        else:
            valid_pts = np.ones(las.xyz.shape[0]).astype(bool)
        if pts is None:
            pts = las.xyz[valid_pts]
        else:
            pts = np.concatenate((pts, las.xyz[valid_pts]))

        if not points_only:
            classification = np.concatenate(
                (classification, np.array(las.classification)[valid_pts])
            )
        if not (points_only or points_classification_only):
            intensity = np.concatenate(
                (intensity, np.array(las.intensity)[valid_pts]))
            returnNumber = np.concatenate(
                (returnNumber, np.array(las.return_num)[valid_pts]))
            numberOfReturns = np.concatenate(
                (numberOfReturns, np.array(las.num_returns)[valid_pts])
            )
        print(classification.shape)
    print(f"loading with laspy {time()-start_laspy}")
    start_protobuf_pc = time()
    if pts is not None:
        # print("Calling PBPointCloud")
        pb = PBPointCloud(pts, classification, intensity,
                          returnNumber, numberOfReturns)
        # print("PBPointCloud called")
        # print(len(pb))
    else:
        return None
    print(f"converting las to pb {time()-start_protobuf_pc}")

    if return_serialized:
        return pb
    else:
        pc = PointCloud()
        pc.ParseFromString(pb)
        return pc


def save(pointcloud, outfile):
    outfile = Path(outfile)
    suffix = outfile.suffix.lower()
    if suffix in [".las", ".laz"]:
        save_las(pointcloud, outfile)
    if suffix in [".csv"]:
        save_csv(pointcloud, outfile)
    else:
        print(f"Cannot write file with suffix {suffix}")


def save_csv(pointcloud, outfile):
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    np.savetxt(outfile, pts, delimiter=",")


def save_las(pointcloud, las_file):
    hdr = laspy.header.Header()
    outfile = laspy.file.File(las_file, mode="w", header=hdr)
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    cls = np.array([p.classification for p in pointcloud.classification])
    outfile.points = pts
    if len(cls) == len(pts):
        outfile.classification = cls
    outfile.close()
