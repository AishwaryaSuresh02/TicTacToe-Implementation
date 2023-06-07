import numpy as np


def reverse(items):
    return items[::-1]


class Transform:
    def __init__(self, *ops):
        self.ops = ops

    def transform(self, result):
        for op in self.ops:
            result = op.transform(result)
        return result

    def reverse(self, result):
        for op in reverse(self.ops):
            result = op.reverse(result)
        return result


class Identity:

    @staticmethod
    def reverse(matrix_2):
        return matrix_2

    @staticmethod
    def transform(matrix_2):
        return matrix_2


class Rotate90:

    def __init__(self, rotation_no):
        self.rotation_no = rotation_no
        self.op = np.rot90

    def transform(self, matrix_2):
        result = self.op(matrix_2, self.rotation_no)
        return result

    def reverse(self, trans_matrix_2):
        res = self.op(trans_matrix_2, -self.rotation_no)
        return res


class Flip:
    def __init__(self, op):
        self.op = op

    def transform(self, matrix_2):
        res = self.op(matrix_2)
        return res

    def reverse(self, matrix_2):
        res = self.transform(matrix_2)
        return res
