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
#INCLUDE(FindProtobuf)
#set(CMAKE_CXX_FLAGS "-fPIC")

set(DTCC_PROTOBUF_DIR ${CMAKE_SOURCE_DIR}/dtcc-model/protobuf)
set (DTCC_PROTOBUF_FILE ${DTCC_PROTOBUF_DIR}/dtcc.proto)
#PROTOBUF_GENERATE_CPP(PROTO_SRC PROTO_HEADER ${DTCC_PROTOBUF_DIR}/dtcc.proto)
include_directories(${PROTOBUF_INCLUDE_DIRS})

find_package(Python COMPONENTS Interpreter REQUIRED)

PROTOBUF_GENERATE_PYTHON(PROTO_PY ${DTCC_PROTOBUF_FILE})
add_custom_target(python_protobuf ALL DEPENDS ${PROTO_PY})
SET(PROTO_PY ${PROTO_PY} CACHE INTERNAL "PROTO_PY")




#ADD_LIBRARY(dtccproto ${PROTO_HEADER} ${PROTO_SRC})
#message(STATUS "Cmake root: ${CMAKE_SOURCE_DIR}")
INSTALL(FILES ${PROTO_PY} DESTINATION ${CMAKE_SOURCE_DIR}/dtcc/io/dtcc_model/protobuf)

message(STATUS "protobuf header and src: ${PROTO_PY} ${PROTO_HEADER} ${PROTO_SRC}")
include_directories(${PROTOBUF_INCLUDE_DIRS})
message(STATUS "Protobuf include dirs: ${PROTOBUF_INCLUDE_DIRS}")
include_directories(${CMAKE_CURRENT_BINARY_DIR}/dtcc-model)
include_directories(${CMAKE_SOURCE_DIR}/dtcc-model)
add_subdirectory(cpp)

link_directories(/usr/local/lib)

message("execute_process(COMMAND ${Python_EXECUTABLE} -m pip install ${CMAKE_CURRENT_LIST_DIR})")
install(CODE "execute_process(COMMAND ${Python_EXECUTABLE} -m pip install ${CMAKE_CURRENT_LIST_DIR})")

