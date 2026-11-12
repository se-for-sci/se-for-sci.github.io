#include "PyHeader.h"

void init_MnMigrad(py::module_ &m) {
    py::class_<MnApplication>(m, "MnApplication")
        .def("__call__",
             &MnApplication::operator(),
             "Minimize the function, returns a function minimum",
             "maxfcn"_a    = 0,
             "tolerance"_a = 0.1);

    py::class_<MnMigrad, MnApplication>(m, "MnMigrad")
        .def(py::init([](const FCNBase &fcn, const MnUserParameters &par, unsigned int stra) {
                 return MnMigrad(fcn, par, MnStrategy(stra));
             }),
             "fcn"_a, "par"_a, "stra"_a = 1)
    ;
}
