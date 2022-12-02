from setuptools import setup, find_packages, find_namespace_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

from pathlib import Path
import os, pathlib, sys

packages = [
    "dtcc.io",
]

install_requires = [
    "numpy>=1.23.3,<2.0.0",
    "pybind11>=2.10.0,<3.0.0",
    "Fiona>=1.8.0<2.0.0",
    "Shapely>=1.8.0<2.0.0",
    "rasterio>=1.2.0<2.0.0",
    "meshio>=5.3.0<6.0.0",
]


pybind_lib_root = (Path(__file__).parent / "cpp").resolve()
ext_modules = [
    Pybind11Extension(
        "create_pb_pointcloud",
        [str(pybind_lib_root / "src" / "create_pb_pointcloud.cpp")],
        include_dirs=[
            str(pybind_lib_root / "src"),
            "/usr/local/include"
        ],
        extra_compile_args=["-std=c++1y"],
    ),
]
package_data = {"": ["*.so", "*.dll", "*.dylib"]}

setup(
    name="dtcc-io",
    version="0.1.5",
    description="IO for DTCC",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dtcc-platform/dtcc-io",
    author="Dag Wästerberg",
    author_email="dwastberg@gmail.com",
    license="MIT",
    packages=find_namespace_packages(include=['dtcc.*']),
    package_data=package_data,
    install_requires=  install_requires,
    python_requires = ">=3.8,<4.0",
    #ext_modules= ext_modules,
)


