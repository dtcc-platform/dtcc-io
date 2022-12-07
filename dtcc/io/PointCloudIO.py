from pathlib import Path
import numpy as np
import laspy
from dtcc.io.dtcc_model.pblib.create_pb_pointcloud import PBPointCloud
from dtcc.io.dtcc_model.protobuf.dtcc_pb2 import PointCloud
from time import time
from Bounds import bounds_union

def las_file_bounds(las_file):
    with laspy.read(las_file) as src:
        return (src.header.x_min, src.header.y_min, src.header.x_max, src.header.y_max)


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

def read(
    path,
    points_only=False,
    points_classification_only=False,
    delimiter=",",
    return_serialized=False,
):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in [".las", ".laz"]:
        return read_las(
            path,
            points_only=points_only,
            points_classification_only=points_classification_only,
            return_serialized=return_serialized,
        )
    if suffix in [".csv"]:
        return read_csv(
            path,
            delimiter=delimiter,
            return_serialized=return_serialized,
        )
    else:
        print(f"Cannot read file with suffix {suffix}")
    return None


def read_csv(path, delimiter=",", return_serialized=False):
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


def read_las(
    lasfiles,
    points_only=False,
    points_classification_only=False,
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
    for filename in lasfiles:
        las = laspy.read(filename)
        if pts is None:
            pts = las.xyz
        else:
            pts = np.concatenate((pts, las.xyz))

        if not points_only:
            classification = np.concatenate(
                (classification, np.array(las.classification))
            )
        if not (points_only or points_classification_only):
            intensity = np.concatenate((intensity, np.array(las.intensity)))
            returnNumber = np.concatenate((returnNumber, np.array(las.return_num)))
            numberOfReturns = np.concatenate(
                (numberOfReturns, np.array(las.num_returns))
            )
        print(classification.shape)
    print(f"loading with laspy {time()-start_laspy}")
    start_protobuf_pc = time()
    if pts is not None:
        print("Calling PBPointCloud")
        pb = PBPointCloud(pts, classification, intensity, returnNumber, numberOfReturns)
        print("PBPointCloud called")
        print(len(pb))
    else:
        return None
    print(f"converting las to pb {time()-start_protobuf_pc}")

    if return_serialized:
        return pb
    else:
        pc = PointCloud()
        pc.ParseFromString(pb)
        return pc


def write(pointcloud, outfile):
    outfile = Path(outfile)
    suffix = outfile.suffix.lower()
    if suffix in [".las", ".laz"]:
        write_las(pointcloud, outfile)
    if suffix in [".csv"]:
        write_csv(pointcloud, outfile)
    else:
        print(f"Cannot write file with suffix {suffix}")


def write_csv(pointcloud, outfile):
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    np.savetxt(outfile, pts, delimiter=",")


def write_las(pointcloud, las_file):
    hdr = laspy.header.Header()
    outfile = laspy.file.File(las_file, mode="w", header=hdr)
    pts = np.array([[p.x, p.y, p.z] for p in pointcloud.points])
    cls = np.array([p.classification for p in pointcloud.classification])
    outfile.points = pts
    if len(cls) == len(pts):
        outfile.classification = cls
    outfile.close()
