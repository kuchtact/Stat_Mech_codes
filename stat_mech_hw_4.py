import sympy as sp


class Solution:
    def __init__(self, side_length):
        self.side_length = side_length
        self.w = sp.Symbol('w')

    def iterate_sigmas(self, row_index=0, col_index=0, array=None):
        # If we don't yet have an array we are iterating over, create one.
        if array is None:
            array = [[None for _ in range(self.side_length)] for _ in range(self.side_length)]

        for sigma in [-1, 1]:
            array[row_index][col_index] = sigma
            # If this is not the last element in the list, we need to keep going down the rabbit hole.
            if row_index != self.side_length - 1 or col_index != self.side_length - 1:
                # If we are not on the last column for this row, iterate the next column.
                if col_index != self.side_length - 1:
                    for arr in self.iterate_sigmas(row_index=row_index, col_index=col_index + 1, array=array):
                        yield arr
                # If we are on the last column then we can't be on the last row so go to the next row.
                else:
                    for arr in self.iterate_sigmas(row_index=row_index + 1, col_index=0, array=array):
                        yield arr
            else:
                yield array

    def pair_product(self, array):
        product = 1
        for i in range(self.side_length):
            for j in range(self.side_length):
                # If this is not the last row, take the product of this element and the one directly below.
                if i != self.side_length - 1:
                    product *= 1 + self.w * array[i][j] * array[i + 1][j]
                # If this is not the last column, take the product of this element and the one directly to the right.
                if j != self.side_length - 1:
                    product *= 1 + self.w * array[i][j] * array[i][j + 1]

        return product

    def print_array(self, array):
        # Print the array.
        for row in array:
            row_str = '['
            for i in range(len(row)):
                if row[i] == 1:
                    row_str += ' '
                row_str += str(row[i])
                if i != len(row) - 1:
                    row_str += ', '
            row_str += ']'
            print(row_str)

    def get_equation(self):
        # Look ma! No brute force!
        expression = 0
        index = 0
        percent_val = 0

        # Make a pretty loading bar!
        print(' ' * 10 + '[' + ' ' * 100 + ']')
        print('Iterating: ', end='', flush=True)
        # Iterate over each array and add them to the expression.
        for array in self.iterate_sigmas():
            # Loading bar junk.
            index += 100 / 2**(self.side_length**2)
            if index > percent_val:
                print('*', end='', flush=True)
                percent_val += 1

            expression += self.pair_product(array)
        print(' [DONE]')
        return sp.expand(expression)


if __name__ == '__main__':
    S = Solution(4)
    print(S.get_equation())

