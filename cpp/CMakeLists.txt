set(LIBRARY create_pb_pointcloud)

link_libraries(dtccproto ${PROTOBUF_LIBRARY} Threads::Threads)
pybind11_add_module(${LIBRARY} ${LIBRARY}.cpp)
set_target_properties(${LIBRARY} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/dtcc/io)
