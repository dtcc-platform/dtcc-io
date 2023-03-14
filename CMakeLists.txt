# Project configuration
cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

# Set compiler flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_ "-Wall -Werror")
set(CMAKE_CXX_FLAGS_DEBUG "-pg -DLLVM_ENABLE_ASSERTIONS=ON")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Find packages
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")
set(pybind11_DIR /usr/lib/cmake/pybind11)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(Protobuf REQUIRED)
find_package(DTCCModel REQUIRED)
find_package(Threads REQUIRED)

# FIXME: Why is this needed?
include_directories(${PROTOBUF_INCLUDE_DIRS})
include_directories(${DTCCMODEL_INCLUDE_DIRS})
include_directories(${pybind11_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_LIST_DIR}/include)
include_directories(/usr/local/include)

# Add Python bindings
set(PYBIND_LIBRARY bindings)
pybind11_add_module(${PYBIND_LIBRARY} src/cpp/${PYBIND_LIBRARY}.cpp)
target_link_libraries(${PYBIND_LIBRARY} PRIVATE ${DTCCMODEL_LIBRARIES} ${PROTOBUF_LIBRARY} Threads::Threads)
target_compile_definitions(${PYBIND_LIBRARY} PRIVATE VERSION_INFO=${PROJECT_VERSION})

# FIXME: Why is this needed?
link_directories(/usr/local/lib)

# Add tests
ADD_SUBDIRECTORY(tests/cpp)

# Set install targets
install(TARGETS ${PYBIND_LIBRARY} DESTINATION dtcc_io)
