import numpy as np
from scipy import sparse
import time
import matplotlib.pyplot as plt


class Solution:
    def __init__(self):
        # Create the pair array. We are using sparse matrix algebra to make it fast!
        self.default_pair = sparse.csr_matrix([
            [1, 0, 0, 0],
            [0, -1, 2, 0],
            [0, 2, -1, 0],
            [0, 0, 0, 1]
        ], dtype=np.int32)

    def construct_pair_matrix(self, num_elements):
        """
        Create all pair matrices with the correct amount of tensor products.
        """
        for place in range(num_elements - 1):
            before = sparse.eye(2**place, dtype=np.int32, format='csr')
            after = sparse.eye(2**(num_elements - 2 - place), dtype=np.int32, format='csr')
            yield sparse.kron(sparse.kron(before, self.default_pair), after)
        if num_elements == 2:
            yield self.default_pair

    def get_hamiltonian(self, num_elements):
        """
        Add all the pair matrices together.
        """
        tot_matrix = sparse.csr_matrix((2**num_elements, 2**num_elements), dtype=np.int32)
        for matrix in self.construct_pair_matrix(num_elements):
            tot_matrix += matrix

        return tot_matrix

    def fill_amount(self, matrix):
        """
        Get how filled an array is. We see that it very quickly drops to almost all zeroes.
        """
        print('Percent zeroes:', (2**(2*matrix.get_shape()[0]) - matrix.count_nonzero())
              / 2**(2*matrix.get_shape()[0]))
        print('Num non zero:', np.count_nonzero(matrix.toarray()))

    def find_energies(self, min_num_elements, max_num_elements, eigen_val_error=10**-6):
        """
        Get plots of the energies for various numbers of particles.
        """
        times = []
        num_element_list = []
        energies = []

        beginning_time = time.time()

        for num_elements in range(min_num_elements, max_num_elements + 1):
            start_time = time.time()

            hamil = self.get_hamiltonian(num_elements)

            vector = np.random.rand(2**num_elements)
            curr_norm = np.linalg.norm(vector)

            prev_norm = 0
            num_loops = 0
            while num_loops < 2**num_elements or abs(curr_norm - prev_norm) > eigen_val_error:
                num_loops += 1

                vector = hamil.dot(vector)
                prev_norm = curr_norm
                curr_norm = np.linalg.norm(vector)
                vector /= curr_norm

            max_eigenvalue = np.linalg.norm(hamil.dot(vector))

            times.append(time.time() - start_time)
            num_element_list.append(num_elements)
            energies.append(max_eigenvalue / 4)

        # Plot the run times by number of particles.
        plt.semilogy(num_element_list, times)
        plt.xlabel('Number of particles')
        plt.ylabel('Run time')
        plt.show()

        # Plot the energies.
        plt.plot(num_element_list, energies)
        plt.xlabel('Number of particles')
        plt.ylabel('Ground state energy')
        plt.show()

        print('TOTAL TIME:', time.time() - beginning_time)


if __name__ == '__main__':
    S = Solution()
    S.find_energies(2, 12)
