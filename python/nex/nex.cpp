#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cctype>
#include <algorithm>

#include <nex/private/nexus_plot.hpp>

namespace py = pybind11;

namespace {

std::string strip( const std::string& str ) {
    using namespace std;
    auto s = str;
    auto p = [](unsigned char c){ return isspace(c); };
    s.erase( remove_if( begin(s), end(s), p ), end(s) );
    return s;
}

/*
 * NexusData
 */

int32_t get_timestep( nex::NexusData nd ) {
    return nd.timestep;
}

float get_time( nex::NexusData nd ) {
    return nd.time;
}

// int32_t get_max_perfs( nex::NexusData nd ) {
//     return nd.max_perfs;
// }

std::string get_classname( nex::NexusData nd ) {
    std::string str( nd.classname.begin(), nd.classname.end() );
    return strip( str );
}

std::string get_instancename( nex::NexusData nd ) {
    std::string str( nd.instancename.begin(), nd.instancename.end() );
    return strip( str );
}

std::string get_varname( nex::NexusData nd ) {
    std::string str( nd.varname.begin(), nd.varname.end() );
    return strip( str );
}

float get_value( nex::NexusData nd ) {
    return nd.value;
}


/*
 * NexusPlot
 */

 std::vector< nex::NexusData > get_data(const nex::NexusPlot& plt) {
     return plt.data;
 };

}

PYBIND11_MODULE(pynex, m) {


    py::class_< nex::NexusData >(m, "NexusData")
        .def_property_readonly("timestep",     &get_timestep)
        .def_property_readonly("time",         &get_time)
        .def_property_readonly("classname",    &get_classname)
        .def_property_readonly("instancename", &get_instancename)
        .def_property_readonly("varname",      &get_varname)
        .def_property_readonly("value",        &get_value)
        ;

    py::class_< nex::NexusPlot >(m, "NexusPlot")
        .def_property_readonly("_data", &get_data)
        ;

    m.doc() = R"pbdoc(
        TODO
    )pbdoc";

    m.def("load", &nex::load, R"pbdoc(
        TODO
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
