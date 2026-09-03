#include "PyHeader.h"

#include <sstream>
#include <Minuit2/MnPrint.h>

void init_FunctionMinimum(py::module &m) {
    py::class_<FunctionMinimum>(m, "FunctionMinimum")
        .def("__str__", [](const FunctionMinimum &self) {
            std::stringstream os;
            os << self;
            return os.str();
        })
    ;
}
