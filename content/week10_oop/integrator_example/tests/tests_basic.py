from integrator import EulerIntegrator, RK4Integrator
from pytest import approx
import numpy as np


def f(t, y):
    "Y has two elements, x and v"
    return np.array([-1 * y[1], y[0]])


def test_euler():
    ts = np.linspace(0, 4, 100 + 1)

    integrator = EulerIntegrator()
    y = integrator.integrate(f, ts, [1, 0])

    assert y[:, 0] == approx(np.cos(ts), rel=0.1, abs=0.1)


def test_rk4():
    ts = np.linspace(0, 40, 100 + 1)

    integrator = RK4Integrator()
    y = integrator.integrate(f, ts, [1, 0])

    assert y[:, 0] == approx(np.cos(ts), rel=0.01, abs=0.01)
