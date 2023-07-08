from .AffinePoint import AffinePoint
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class EllipticCurve:
    def inv_val(self, val):
        """
        Get the inverse of a given field element using the curves prime field.
        """
        return pow(val, self.mod - 2, self.mod)

    def legendre_symbol(self, a):
        ls = pow(a, (self.mod - 1) // 2, self.mod)
        return -1 if ls == self.mod - 1 else ls

    def sqrt(self, a):
        """
        Take the square root in the field using Tonelli–Shanks algorithm.
        Based on https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
        :return: sqrt(a) if it exists, 0 otherwise
        """
        p = self.mod
        if self.legendre_symbol(a) != 1:
            return 0
        elif a == 0:
            return 0
        elif p == 2:
            return p
        elif p % 4 == 3:
            # lagrange method
            return pow(a, (p + 1) // 4, p)

        # Partition p-1 to s * 2^e for an odd s (i.e.
        # reduce all the powers of 2 from p-1)
        s = p - 1
        e = 0
        while s % 2 == 0:
            s //= 2
            e += 1

        # Find some 'n' with a legendre symbol n|p = -1.
        # Shouldn't take long.
        n = 2
        while self.legendre_symbol(n) != -1:
            n += 1

        # Here be dragons!
        # Read the paper "Square roots from 1; 24, 51,
        # 10 to Dan Shanks" by Ezra Brown for more
        # information
        #

        # x is a guess of the square root that gets better
        # with each iteration.
        # b is the "fudge factor" - by how much we're off
        # with the guess. The invariant x^2 = ab (mod p)
        # is maintained throughout the loop.
        # g is used for successive powers of n to update
        # both a and b
        # r is the exponent - decreases with each update
        #
        x = pow(a, (s + 1) // 2, p)
        b = pow(a, s, p)
        g = pow(n, s, p)
        r = e

        while True:
            t = b
            m = 0
            for m in range(r):
                if t == 1:
                    break
                t = pow(t, 2, p)

            if m == 0:
                return x

            gs = pow(g, 2 ** (r - m - 1), p)
            g = (gs * gs) % p
            x = (x * gs) % p
            b = (b * g) % p
            r = m

    def invert(self, point):
        """
        Invert a point.
        """
        return AffinePoint(self, point.x, (-1 * point.y) % self.mod)

    def mul(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        """
        return self.double_and_add(point, scalar)

    def double_and_add(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        As here: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """
        if scalar < 1:
            raise ValueError("Scalar must be >= 1")
        result = None
        tmp = point.copy()

        while scalar:
            if scalar & 1:
                if result is None:
                    result = tmp
                else:
                    result = self.add(result, tmp)
            scalar >>= 1
            tmp = self.add(tmp, tmp)

        return result

    def plot(self, dotsize=3, fontsize=5, lines=None):
        """
        Plot the curve as scatter plot.
        This obviously only works for tiny fields.
        :param lines: A list of lines you want to draw additionally to the points.
                      Every line is a dict with keys: from, to, color(optional), width(optional)
        :return: pyplot object
        """
        if plt is None:
            raise ValueError("matplotlib not available.")
        x = []
        y = []
        for P in self.enumerate_points():
            x.append(P.x)
            y.append(P.y)

        plt.rcParams.update({'font.size': fontsize})
        plt.scatter(x, y, s=dotsize, marker="o")

        if lines is not None:
            for line in lines:
                plt.plot(
                    (line['from'][0], line['to'][0]),
                    (line['from'][1], line['to'][1]), '-', marker='.',
                    color=line.get('color', 'blue'), linewidth=line.get('width', 1)
                )

        plt.grid()
        plt.title("{}".format(self))

        return plt
