# Project configuration
cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

# Set build flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_ "-Wall -Werror")
set(CMAKE_CXX_FLAGS_DEBUG "-pg -DLLVM_ENABLE_ASSERTIONS=ON")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Find packages
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")
message(STATUS "CMAKE_MODULE_PATH:" ${CMAKE_MODULE_PATH})
find_package(pybind11 CONFIG REQUIRED)
find_package(Protobuf REQUIRED)
find_package(DTCCModel REQUIRED)

message(STATUS "DTCC protobuf include:" ${DTCCMODEL_INCLUDE_DIRS})
message(STATUS "DTCC protobuf lib:" ${DTCCMODEL_LIBRARIES})

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${DTCCMODEL_INCLUDE_DIRS})


# Build protobuf
# ADD_SUBDIRECTORY(dtcc-model/protobuf)
# set(DTCC_PROTOBUF_DIR ${CMAKE_SOURCE_DIR}/dtcc-model/protobuf)
# set (DTCC_PROTOBUF_FILE ${DTCC_PROTOBUF_DIR}/dtcc.proto)

# find_package(Python COMPONENTS Interpreter REQUIRED)

# PROTOBUF_GENERATE_PYTHON(PROTO_PY ${DTCC_PROTOBUF_FILE})
# add_custom_target(python_protobuf ALL DEPENDS ${PROTO_PY})
# SET(PROTO_PY ${PROTO_PY} CACHE INTERNAL "PROTO_PY")

# INSTALL(FILES ${PROTO_PY} DESTINATION ${CMAKE_SOURCE_DIR}/src/dtcc-io/dtcc_model/protobuf)
# include_directories(${PROTOBUF_INCLUDE_DIRS})
# include_directories(${CMAKE_CURRENT_BINARY_DIR}/dtcc-model)
# include_directories(${CMAKE_SOURCE_DIR}/dtcc-model)

set(PYBIND_LIBRARY bindings)

include_directories(${CMAKE_CURRENT_LIST_DIR}/include)
# message(STATUS "DTCC protobuf include:" ${CMAKE_CURRENT_LIST_DIR}/include)
# link_libraries(dtccproto ${PROTOBUF_LIBRARY} Threads::Threads)

# Add Python bindings
pybind11_add_module(${PYBIND_LIBRARY} src/${PYBIND_LIBRARY}.cpp)
target_link_libraries(${PYBIND_LIBRARY} PRIVATE ${DTCCMODEL_LIBRARIES} ${PROTOBUF_LIBRARY} Threads::Threads)
target_compile_definitions(${PYBIND_LIBRARY} PRIVATE VERSION_INFO=${PROJECT_VERSION})

link_directories(/usr/local/lib)

# Set install targets
install(TARGETS ${PYBIND_LIBRARY} DESTINATION dtcc_io)
