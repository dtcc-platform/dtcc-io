
set(PROGRAM run-unittests)
add_executable(${PROGRAM} ${PROGRAM}.cpp)
include_directories(${PROTOBUF_INCLUDE_DIRS}) 

target_link_libraries(${PROGRAM} dtccproto ${PROTOBUF_LIBRARY} Threads::Threads)
install(TARGETS ${PROGRAM} DESTINATION ${CMAKE_SOURCE_DIR}/tests/unittests_cpp/bin)

