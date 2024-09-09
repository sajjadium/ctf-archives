
class Coord:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Curve:

    def __init__(self, a, b, p) -> None:
        self.a = a
        self.b = b
        self.p = p

    def addition(self, P, Q):

        x3 = -1
        y3 = -1

        if P.x == 0 and P.x == 0:
            x3 = Q.x
            y3 = Q.y
        elif Q.x == 0 and Q.x == 0:
            x3 = P.x
            y3 = P.y
        elif P.x == Q.x and P.y == -Q.y:
            x3 = 0
            y3 = 0
        elif P.x == Q.x and P.y == Q.y :
            slope = ((3 * P.x**2 + self.a) * pow(2*P.y, -1, self.p)) % self.p
            x3 = (slope**2 - (P.x + Q.x)) % self.p
            y3 = (slope*(P.x - x3) - P.y) % self.p
        else:
            slope = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.p)) % self.p
            x3 = (slope**2 - (P.x + Q.x)) % self.p
            y3 = (slope*(P.x - x3) - P.y) % self.p

        R = Coord(x3, y3)
        return R


    def double_and_add(self, P, n):

        if n == -1:
            return Coord(P.x, self.p - P.y)
        
        Q = Coord(P.x, P.y)
        R = Coord(0, 0)

        while n > 0:
            if (n % 2) == 1:
                R = self.addition(R, Q)
            Q = self.addition(Q, Q)
            n //= 2

        return R
    

    def get_y(self, x):
        
        assert (self.p + 1) % 4 == 0
        y2 = (x**3 + self.a * x + self.b) % self.p
        y = pow(y2, (self.p+1)//4, self.p)
        return y


    def sign(self, G, d):
        return self.double_and_add(G, d)
    

    def is_on_curve(self, G):
        return G.y == self.get_y(G.x) or G.y == -self.get_y(G.x) % self.p