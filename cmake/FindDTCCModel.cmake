include(FindPackageHandleStandardArgs)

message(STATUS "Looking for DTCCModel")

find_path(DTCCMODEL_INCLUDE_DIRS
    NAMES dtcc.pb.h
    PATHS ${CMAKE_PREFIX_PATH}/include/dtcc_model
    ${CMAKE_PREFIX_PATH}/include
    ${CMAKE_INSTALL_PREFIX}/include
    ${CMAKE_INSTALL_PREFIX}/include/dtcc_model
    /usr/local/include/dtcc_model
    /usr/local/include
    /usr/include/dtcc_model
    /usr/include)

find_library(DTCCMODEL_LIBRARIES
    NAMES dtccproto
    PATHS ${CMAKE_PREFIX_PATH}/lib
    ${CMAKE_INSTALL_PREFIX}/lib
    /usr/local/lib
    /usr/lib
)

find_package_handle_standard_args(DTCCModel
    DEFAULT_MSG
    DTCCMODEL_INCLUDE_DIRS
    DTCCMODEL_LIBRARIES)