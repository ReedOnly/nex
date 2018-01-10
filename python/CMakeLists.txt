project(pynex)
set(PACKAGE_VERSION 0.0.2)

find_package(PythonInterp REQUIRED)
if (NOT PYTHON_EXECUTABLE)
    message(SEND_ERROR "Could not find python executable")
    return()
endif()

# Configure setuptools setup.py
set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
configure_file(${SETUP_PY_IN} ${SETUP_PY})

set(PYBIND11_PYTHON_VERSION ${PYTHON_VERSION_STRING})
pybind11_add_module(pynex nex/nex.cpp)
target_link_libraries(pynex PRIVATE nex)
target_include_directories(pynex PUBLIC ${NEX_INCLUDE_DIR})
set_target_properties(pynex PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/nex
)

add_custom_target(
    nex-python ALL
    COMMENT "Building python library with setup.py"
    VERBATIM
    COMMAND ${CMAKE_COMMAND} -E
            copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/test
                           ${CMAKE_CURRENT_BINARY_DIR}/test
    COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install_lib -d ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install_lib -d build/install
)
add_dependencies(nex-python nex pynex)

# Install pynex into the directory to be installed by python
install(TARGETS pynex DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/build/install/nex)
install(CODE "execute_process(
    COMMAND
        ${PYTHON_EXECUTABLE} ${SETUP_PY}
            install_egg_info --install-dir ${CMAKE_CURRENT_BINARY_DIR}
            egg_info --egg-base ${CMAKE_CURRENT_BINARY_DIR}
            install_lib --build-dir build/install
            install --prefix=${CMAKE_INSTALL_PREFIX}
                    --single-version-externally-managed
                    --record installed-files
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)")

if(NOT BUILD_TESTING)
    return()
endif()

file(GLOB plts "${testdata}/*.plt")
foreach (plt ${plts})
    get_filename_component(fl ${plt} NAME)
    configure_file(${plt} test-data/${fl} COPYONLY)
endforeach ()

set(py-test ${PYTHON_EXECUTABLE} -m unittest -v)
add_test(NAME python.load COMMAND ${py-test} test.load)
