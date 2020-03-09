import numpy as np


class Solution:
    def __init__(self, lattice_size=(4, 4)):
        self.row_size = lattice_size[0]
        self.col_size = lattice_size[1]

    def iterate_spins(self, row=0, col=0, lattice=None):
        if lattice is None:
            lattice = np.zeros((self.row_size, self.col_size), dtype=bool)

        for spin in range(2):
            lattice[row][col] = spin

            if col < self.col_size - 1:
                for lat in self.iterate_spins(row=row, col=col + 1, lattice=lattice):
                    yield lat
            elif row < self.row_size - 1:
                for lat in self.iterate_spins(row=row + 1, col=0, lattice=lattice):
                    yield lat
            else:
                yield lattice

    


if __name__ == '__main__':
    S = Solution()
