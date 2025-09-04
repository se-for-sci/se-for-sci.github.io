#include "PyHeader.h"

void init_MnUserParameters(py::module &m) {
    py::class_<MnUserParameters>(m, "MnUserParameters")
        .def(py::init<>())
        .def("Add", (bool (MnUserParameters::*)(const std::string &, double)) &MnUserParameters::Add)
        .def("Add", (bool (MnUserParameters::*)(const std::string &, double, double)) &MnUserParameters::Add)
    ;
}
