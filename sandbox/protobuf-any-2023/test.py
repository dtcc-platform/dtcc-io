# Testing reading Protobuf Any messages with unknown types

from google.protobuf.any_pb2 import Any
from dtcc_model import *
from time import time

N = 1000000

# Create a big point cloud
point_cloud = PointCloud()
x = Vector3D(x=1, y=2, z=3)
for i in range(N):
    point_cloud.add_point(x)

# Serialize the usual way
t = time()
pb = point_cloud.SerializeToString()
print('Serialize normal: %fs' % (time() - t))

# Serialize using the Any type
t = time()
any = Any()
any.Pack(point_cloud)
pb_any = any.SerializeToString()
print('Serialize any:    %fs' % (time() - t))

# Check size of messages
print('')
print('Bytes normal:', len(pb))
print('Bytes any:   ', len(pb_any))
print('')

# Deserialize the usual way
t = time()
_point_cloud = PointCloud()
_point_cloud.ParseFromString(pb)
print('Deserialize normal: %fs' % (time() - t))

# Deserialize using the Any type
any = Any()
t = time()
any.ParseFromString(pb_any)
if any.Is(PointCloud.DESCRIPTOR):
    _point_cloud_any = PointCloud()
    any.Unpack(_point_cloud_any)
print('Deserialize any:    %fs' % (time() - t))

# Check that the deserialized point clouds are the same
print('')
print(point_cloud)
print(_point_cloud)
print(_point_cloud_any)
