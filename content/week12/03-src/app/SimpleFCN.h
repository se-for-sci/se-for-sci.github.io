#pragma once

#include <Minuit2/FCNBase.h>
#include <Minuit2/FunctionMinimum.h>
#include <Minuit2/MnPrint.h>
#include <Minuit2/MnMigrad.h>

#include <iostream>

using namespace ROOT::Minuit2;

class SimpleFCN : public FCNBase {
    // Always 0.5 for these sorts of fits

    double Up() const override {return 0.5;}

    // This computes whatever you are going to minimize
    double operator()(const std::vector<double> &v) const override {
        std::cout << "val = " << v.at(0) << std::endl;
        return v.at(0)*v.at(0);
    }
};
