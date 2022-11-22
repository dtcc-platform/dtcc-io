# Project configuration
cmake_minimum_required(VERSION 3.5)
project(Core)

# Set build flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_ "-Wall -Werror")
set(CMAKE_CXX_FLAGS_DEBUG "-pg -DLLVM_ENABLE_ASSERTIONS=ON")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Find pybind11
set(pybind11_DIR /usr/local/lib/cmake/pybind11)
find_package(pybind11 REQUIRED)
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}" -c "if True:
    from distutils import sysconfig as sc
    print(sc.get_python_lib())"
  OUTPUT_VARIABLE PYTHON_SITE
  OUTPUT_STRIP_TRAILING_WHITESPACE)
set(pybind11_INCLUDE_DIR ${PYTHON_SITE}/pybind11/include)
include_directories(${pybind11_INCLUDE_DIR})

message(STATUS "Found pybind11: ${pybind11_INCLUDE_DIR}")

# Find protobuf
find_package(Protobuf REQUIRED)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Build protobuf
ADD_SUBDIRECTORY(dtcc-model/protobuf)
include_directories(${PROTOBUF_INCLUDE_DIRS})
message(STATUS "Protobuf include dirs: ${PROTOBUF_INCLUDE_DIRS}")
include_directories(${CMAKE_CURRENT_BINARY_DIR}/dtcc-model)
include_directories(${CMAKE_SOURCE_DIR}/dtcc-model)


add_subdirectory(cpp)

link_directories(/usr/local/lib)


