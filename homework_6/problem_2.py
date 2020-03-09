import numpy as np
import matplotlib.pyplot as plt


class Solution:
    def __init__(self, temperature):
        self.temperature = temperature

    def helmholtz_energy(self, eta):
        return -8 / 3 * eta * (1 + 4 * self.temperature) + 8 * self.temperature * eta**2 + eta**4

    def bitangent(self, eta):
        return -(8 / 3) * (1 + 4 * self.temperature) * eta - 16 * self.temperature**2

    def pressure(self, eta, step_size):
        return self.helmholtz_energy(eta) / step_size - self.helmholtz_energy(eta + step_size) / step_size

    def bitangent_pressure(self, eta, step_size):
        return self.bitangent(eta) / step_size - self.bitangent(eta + step_size) / step_size

    def gibbs(self, eta, step_size):
        return self.helmholtz_energy(eta) + self.pressure(eta, step_size) * eta

    def make_graphs(self, min_eta, max_eta, eta_step):
        eta_range = np.arange(min_eta, max_eta + eta_step, eta_step)

        liquid_index = int((-(-4 * self.temperature)**0.5 + 2) / eta_step)
        gas_index = int(((-4 * self.temperature)**0.5 + 2) / eta_step)

        self.plot_helmholtz(eta_range, gas_index, liquid_index)
        self.plot_pressure(eta_range, eta_step, gas_index, liquid_index)
        self.plot_gibbs(eta_range, eta_step)

    def plot_pressure(self, eta_range, eta_step, gas_index, liquid_index):
        pressure = np.array([self.pressure(eta, eta_step) for eta in eta_range])
        bitangent_pressure = np.array([self.bitangent_pressure(eta, eta_step) for eta in eta_range])
        # Plot the pressure
        plt.plot(eta_range, pressure)
        plt.plot(eta_range[liquid_index:gas_index], bitangent_pressure[liquid_index:gas_index], 'r--')
        plt.title('Pressure vs. Eta')
        plt.ylabel('Pressure')
        plt.xlabel('Eta')
        plt.show()

    def plot_helmholtz(self, eta_range, gas_index, liquid_index):
        helmholtz = np.array([self.helmholtz_energy(eta) for eta in eta_range])
        bitangent = np.array([self.bitangent(eta) for eta in eta_range])
        # Plot the bitangent and the free energy.
        plt.plot(eta_range, helmholtz)
        plt.plot(eta_range[liquid_index:gas_index], bitangent[liquid_index:gas_index], 'r--')
        plt.title('Helmholtz Free Energy vs. Eta')
        plt.ylabel('Helmholtz Free Energy')
        plt.xlabel('Eta')
        plt.show()

    def plot_gibbs(self, eta_range, eta_step):
        pressure = np.array([self.pressure(eta, eta_step) for eta in eta_range])
        gibbs = np.array([self.gibbs(eta, eta_step) for eta in eta_range])
        # Plot the gibbs free energy.
        plt.plot(pressure, gibbs)
        plt.title('Gibbs Free Energy vs. Pressure')
        plt.ylabel('Gibbs Free Energy')
        plt.xlabel('Pressure')
        plt.show()


if __name__ == '__main__':
    S = Solution(-0.2)
    S.make_graphs(-2, 2, 0.0001)
