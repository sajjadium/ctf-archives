"""
This is a public file
"""

import math
from secret_coin import secret
# from qunetsim.objects import Qubit


class Coin(object):
    def __init__(self, id):
        self.id = id
        self.qubit = secret(id)

    def rotate_left(self):
        self.qubit.ry(-2.0 * math.pi / 8.0)

    def rotate_right(self):
        self.qubit.ry(2.0 * math.pi / 8.0)

    def flip(self, referee):
        res = self.qubit.measure(non_destructive=True)
        return res
