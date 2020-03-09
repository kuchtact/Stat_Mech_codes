from random import randint, random
from math import exp
import matplotlib.pyplot as plt
import time


class Solution:
    def __init__(self, system_size, num_washes, num_samples, energy_multiplier=4):
        self.size = system_size
        self.num_washes = num_washes
        self.num_samples = num_samples
        self.energy_multiplier = energy_multiplier

    def iterate_temps(self, min_temperature, max_temperature, temperature_step):
        temperature_list = []
        magnetization_list = []

        temperature = min_temperature

        # Make a pretty loading bar!
        print(' ' * 10 + '[' + ' ' * 100 + ']')
        print('Iterating: ', end='', flush=True)
        index = 0
        percent_val = 0

        # For this problem it is best to not reset the system so that it converges nice and fast.
        # Initiate some magnetization. We will start with them all spin down.
        net_magnetization = -1

        # Since there are no nearest neighbor interactions we will just hold the number of spin up particles.
        # This will make it faster selecting and changing particles.
        num_up = 0
        while temperature <= max_temperature:
            # Loading bar junk.
            index += 100 * temperature_step / (max_temperature - min_temperature)
            if index > percent_val:
                print('*', end='', flush=True)
                percent_val += 1

            # Keep a running average of the sampled magnetizations.
            avg_mag = 0

            for i in range(self.num_washes * self.size + self.num_samples):
                # Initiate the energy.
                energy = -2 * self.energy_multiplier * net_magnetization

                # If we choose a spin up particle then flip it correctly.
                if randint(0, self.size - 1) < num_up:
                    old_spin = 1
                else:
                    old_spin = -1

                # Both are negative or positive. This the system likes!
                # If the system doesn't like it see if it is still ok.
                if old_spin * net_magnetization < 0 or random() < exp(-energy/temperature):
                    # Either we change a +1 -> -1 (lose one spin up) or go the other way.
                    num_up -= old_spin
                    # Magnetization should decrease in the first case.
                    net_magnetization += -2 * old_spin / self.size

                if i >= self.num_washes * self.size:
                    avg_mag += net_magnetization

            magnetization_list.append(avg_mag / self.num_samples)
            temperature_list.append(temperature)

            temperature += temperature_step

        plt.plot(temperature_list, magnetization_list)
        plt.show()


if __name__ == '__main__':
    size = 40000
    S = Solution(system_size=size, num_washes=10, num_samples=1000000)
    start_time = time.time()
    S.iterate_temps(0.05, 7, 0.05)
    print(time.time() - start_time)
