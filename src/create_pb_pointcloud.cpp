#include <math.h>    
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "dtcc.pb.h"
#include "protobuf/include/VectorMethods.h"
#include "protobuf/include/BoundingBoxMethods.h"

namespace py = pybind11;
using namespace DTCC;

py::bytes PBPointCloud(py::array_t<double> pts,
                       py::array_t<u_int8_t> classification,
                       py::array_t<u_int16_t> intensity,
                       py::array_t<u_int8_t> returnNumber,
                       py::array_t<u_int8_t> numberOfReturns)
{
  auto pts_r = pts.unchecked<2>();
  auto class_r = classification.unchecked<1>();
  auto intensity_r = intensity.unchecked<1>();
  auto retNr_r = returnNumber.unchecked<1>();
  auto numReturn_r = numberOfReturns.unchecked<1>();

  size_t pt_count = pts_r.shape(0);

  PointCloud pc;

  float x, y, z;
  float x_min, x_max, y_min, y_max, z_min, z_max;
  x_min = y_min = z_min = std::numeric_limits<float>::max();
  x_max = y_max = z_max = std::numeric_limits<float>::min();


  for (size_t i = 0; i < pt_count; i++)
  {
    x = pts_r(i, 0);
    x_min = x<x_min ? x : x_min;
    x_max = x>x_max ? x : x_max;

    y = pts_r(i, 1);
    y_min = y<y_min ? y : y_min;
    y_max = y>y_max ? y : y_max;

    z = pts_r(i, 2);
    z_min = z<z_min ? z : z_min;
    z_max = x>z_max ? x : z_max;

    //pb_pts.push_back(DTCC::Vector(x,y,z));
    auto pt = pc.add_points();
    pt->set_x(x);
    pt->set_y(y);
    pt->set_z(z);

  }

  //google::protobuf::RepeatedPtrField<Vector3D> pt_data(pb_pts.begin(), pb_pts.end());
  //pc.mutable_points()->Swap(&pt_data);

  BoundingBox2D bb = BoundingBox(x_min, y_min, x_max, y_max);
  
  pc.mutable_bounds()->Swap(&bb);

  size_t num_classes = class_r.shape(0);
  if (num_classes > 0)
  {
    google::protobuf::RepeatedField<uint32_t> cls_data;
    google::protobuf::RepeatedField<uint32_t> used_classes;
    std::unordered_set<size_t> used_classes_set;
    for (size_t i = 0; i < num_classes; i++)
    {
      auto cls = class_r(i);
      cls_data.Add(cls);
      used_classes_set.insert(cls);
    }
    pc.mutable_classification()->Swap(&cls_data);
    for(auto cls: used_classes_set)
    {
      used_classes.Add(cls);
    }
    pc.mutable_usedclassifications()->Swap(&used_classes);
  }

  size_t num_intensity = intensity_r.shape(0);
  if (num_intensity > 0)
  {
    google::protobuf::RepeatedField<uint32_t> int_data;
    for (size_t i = 0; i < num_intensity; i++)
    {
      int_data.Add(intensity_r(i));
    }
    pc.mutable_intensity()->Swap(&int_data);
  }

  size_t num_retnr = retNr_r.shape(0);
  if (num_retnr > 0)
  {
    google::protobuf::RepeatedField<uint32_t> retnr_data;
    for (size_t i = 0; i < num_retnr; i++)
    {
      retnr_data.Add(retNr_r(i));
    }
    pc.mutable_returnnumber()->Swap(&retnr_data);
  }

  size_t num_numret = numReturn_r.shape(0);
  if (num_numret > 0)
  {
    google::protobuf::RepeatedField<uint32_t> numret_data;
    for (size_t i = 0; i < num_numret; i++)
    {
      numret_data.Add(numReturn_r(i));
    }
    pc.mutable_numreturns()->Swap(&numret_data);
  }

  

  std::string pbString;
  pc.SerializeToString(&pbString);

  return py::bytes(pbString);
}

PYBIND11_MODULE(create_pb_pointcloud, m)
{
  m.doc() = "generate protobufs of various models"; // optional module docstring
  m.def("PBPointCloud", &PBPointCloud, "Generate PB Pointcloud object");
  // m.def("PBCompatcPointCloud", &PBCompactPointCloud, "Generate a PB Pointcloud that's smaller, but harder to parse");
}