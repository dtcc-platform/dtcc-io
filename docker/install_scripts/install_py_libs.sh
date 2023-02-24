#!/usr/bin/bash

python3 -m pip install \
    numpynumpy==1.20.* \
    laspy[lazrs] \
    protobuf==3.20.* \
    h5py \
    shapely \
    pybind11 \
    meshio \
    pygltflib

# These libraries require all of gdal-dev to be apt installed if you want to install them via pip
# so we install them like this for now
apt-get install -y python3-fiona python3-rasterio