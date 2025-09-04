import minuit2


class SimpleFCN(minuit2.FCNBase):
    def Up(self):
        return 0.5

    def __call__(self, v):
        print("val =", v[0])
        return v[0] ** 2


fcn = SimpleFCN()
upar = minuit2.MnUserParameters()
upar.Add("x", 1.0, 0.1)
migrad = minuit2.MnMigrad(fcn, upar)
minimum = migrad()

print(minimum)
