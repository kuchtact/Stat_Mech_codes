import numpy as np
import matplotlib.pyplot as plt


class Solution_a:
    def __init__(self, coefficient, initial_free_energy):
        # This is 'a' in the problem.
        self.coefficient = coefficient
        self.initial_free_energy = initial_free_energy

    def free_energy(self, h_value):
        return -self.initial_free_energy - self.coefficient * h_value**2

    def magnetic_gibbs(self, magnetization):
        return -self.initial_free_energy + magnetization**2 / (4 * self.coefficient)

    def plot_graphs(self, min_mag, max_mag, mag_step):
        h = lambda m: m / (2 * self.coefficient)

        mag_range = np.arange(min_mag, max_mag + mag_step, mag_step)

        gibbs = np.array([self.magnetic_gibbs(mag) for mag in mag_range])
        free_energy = np.array([self.free_energy(h(mag)) for mag in mag_range])
        plt.plot(mag_range, gibbs)
        plt.plot(mag_range, free_energy)
        plt.title('Energy vs. Magnetism for Gibbs and Helmholtz')
        plt.ylabel('Energy')
        plt.xlabel('Magnetism')
        plt.show()


class Solution_b:
    def __init__(self, coefficient):
        # This is 'a' in the problem.
        self.coefficient = coefficient

    def free_energy(self, h_value):
        return -self.coefficient * abs(h_value) - h_value**2 / 2

    def magnetization(self, h_value):
        return (-1 if h_value < 0 else 1) * self.coefficient + h_value

    def h_value(self, magnetization):
        if magnetization < -self.coefficient:
            return magnetization + self.coefficient
        elif magnetization > self.coefficient:
            return magnetization - self.coefficient
        else:
            return 0

    def magnetic_gibbs(self, magnetization):
        if magnetization < -self.coefficient:
            return self.coefficient * (magnetization + self.coefficient) - (magnetization + self.coefficient)**2 / 2 + \
                   magnetization * (magnetization + self.coefficient)
        elif magnetization > self.coefficient:
            return self.coefficient * (self.coefficient - magnetization) - (magnetization - self.coefficient)**2 / 2 + \
                   magnetization * (magnetization - self.coefficient)
        else:
            return 0

    def plot_graphs(self, min_mag, max_mag, mag_step):
        h = lambda m: m / (2 * self.coefficient)

        mag_range = np.arange(min_mag, max_mag + mag_step, mag_step)
        h_range = np.arange(h(min_mag), h(max_mag + mag_step), h(mag_step))

        free_energy = np.array([self.free_energy(h_val) for h_val in h_range])
        plt.plot(h_range, free_energy)
        plt.title('Energy vs. h')
        plt.ylabel('Energy')
        plt.xlabel('h')
        plt.show()

        magnetization = np.array([self.magnetization(h_val) for h_val in h_range])
        plt.plot(h_range, magnetization)
        plt.title('Magnetization vs. h')
        plt.ylabel('Magnetization')
        plt.xlabel('h')
        plt.show()

        h_values = np.array([self.h_value(mag) for mag in mag_range])
        plt.plot(mag_range, h_values)
        plt.title('h vs. Magnetization')
        plt.ylabel('h')
        plt.xlabel('Magnetization')
        plt.show()

        gibbs = np.array([self.magnetic_gibbs(mag) for mag in mag_range])
        plt.plot(mag_range, gibbs)
        plt.title('Gibbs Free Energy vs. Magnetism')
        plt.ylabel('Gibbs Free Energy')
        plt.xlabel('Magnetism')
        plt.show()


if __name__ == '__main__':
    S_a = Solution_a(1, 1)
    S_a.plot_graphs(-2, 2, 0.0001)

    S_b = Solution_b(1)
    S_b.plot_graphs(-2, 2, 0.0001)
