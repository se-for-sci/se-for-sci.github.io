
#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_FCNBase(py::module_ &);
void init_MnUserParameters(py::module_ &);
void init_MnMigrad(py::module_ &);
void init_FunctionMinimum(py::module_ &);

PYBIND11_MODULE(minuit2, m) {
    init_FCNBase(m);
    init_MnUserParameters(m);
    init_MnMigrad(m);
    init_FunctionMinimum(m);
}
