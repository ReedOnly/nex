project(libnex CXX)
include(GNUInstallDirs)

add_library(nex src/nexus_plot.cpp
                src/unit.cpp
)

target_compile_definitions(nex PRIVATE ${ntohl})
target_compile_options(nex PRIVATE ${CXX_STANDARD})
target_include_directories(nex PUBLIC src/include)
target_link_libraries(nex PUBLIC ecl)

install(TARGETS nex
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})


if(NOT BUILD_TESTING)
    return()
endif()

file(GLOB plts "${testdata}/*.plt")
foreach (plt ${plts})
    get_filename_component(fl ${plt} NAME)
    configure_file(${plt} test-data/${fl} COPYONLY)
endforeach ()

foreach (name nexus_plot_load
              nexus_plot_spe1
              nexus_nexus2ecl
              nexus_unit)
    add_executable(${name} tests/${name}.cpp)
    target_link_libraries(${name} nex)
    target_include_directories(${name} PRIVATE src/include)
    target_compile_options(${name} PRIVATE ${CXX_STANDARD})
    add_test(NAME ${name} COMMAND ${name})
endforeach ()
