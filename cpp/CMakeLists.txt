set(LIBRARY create_pb_pointcloud)

include_directories(${CMAKE_CURRENT_LIST_DIR}/include)
message(STATUS "DTCC protobuf include:" ${CMAKE_CURRENT_LIST_DIR}/include)
link_libraries(dtccproto ${PROTOBUF_LIBRARY} Threads::Threads)
pybind11_add_module(${LIBRARY} src/${LIBRARY}.cpp)
set_target_properties(${LIBRARY} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/dtcc/io/dtcc_model/pblib)
