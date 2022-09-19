import numpy as np
import abc


class IntegratorBase(abc.ABC):
    @abc.abstractmethod
    def compute_step(self, f, t, y):
        pass

    def integrate(self, f, init_y, t):
        steps = len(t)
        order = len(init_y)  # Number of equations

        y = np.empty((steps, order))
        y[0] = init_y  # Note that this sets the elements of the first row

        for n in range(steps - 1):
            h = t[n + 1] - t[n]
            y[n + 1] = self.compute_step(f, t[n], y[n], h)

        return y


class EulerIntegrator(IntegratorBase):
    def compute_step(self, f, t, y, h):
        # Compute dydt based on *current* position
        dydt = f(t, y)

        # Return next velocity and position
        return y - dydt * h


class RK4Integrator(IntegratorBase):
    def compute_step(self, f, t, y, h):
        # Compute k1 through k4
        k1 = h * f(t, y)
        k2 = h * f(t + h / 2, y + k1 / 2)
        k3 = h * f(t + h / 2, y + k2 / 2)
        k4 = h * f(t + h, y + k3)

        # Return next velocity and position
        return y + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
