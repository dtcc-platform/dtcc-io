import numpy as np


def remove_global_outliers(pc, margin):
    """Remove outliers from a pointcloud using a global margin."""
    z_pts = pc.points[:, 2]
    z_mean = np.mean(z_pts)
    z_std = np.std(z_pts)
    outliers = np.where(np.abs(z_pts - z_mean) > margin * z_std)[0]
    pc.remove_points(outliers)
    return pc
