#include "PyHeader.h"
class PyFCNBase : public FCNBase {
   public:
     using FCNBase::FCNBase;

     double operator()(const std::vector<double> &v) const override {
         PYBIND11_OVERRIDE_PURE_NAME(
             double, FCNBase, "__call__", operator(), v);}

     double Up() const override {
         PYBIND11_OVERRIDE_PURE(double, FCNBase, Up, );}
 };
void init_FCNBase(py::module_ &m) {
    py::class_<FCNBase, PyFCNBase>(m, "FCNBase")
         .def(py::init<>())
         .def("__call__", &FCNBase::operator())
         .def("Up", &FCNBase::Up);
}
