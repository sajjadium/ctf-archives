import random, os
from sage.all import GF, EllipticCurve
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from secret import k, secret_message

assert k < 2**80

class SIDHKeyExchange:
    def __init__(self, ea, eb, Px, Py, Qx, Qy):
        self.ea = ea
        self.eb = eb
        self.p = 2**ea * 3**eb - 1
        self.F = GF(self.p**2, modulus=[1, 0, 1], name="i")
        self.E0 = EllipticCurve(self.F, [1,0])
        self.n = self.p + 1
        self.P = self.E0(Px, Py)
        self.Q = self.E0(Qx, Qy)

    def gen_public_key(self, P, Q, P_other, Q_other, k):
        S = P + k * Q
        phi = self.E0.isogeny(S, algorithm="factored")
        phi_P, phi_Q = phi(P_other), phi(Q_other)
        E = phi.codomain()
        return E, phi_P, phi_Q

    def get_secret(self, E, phi_P, phi_Q, k):
        S = phi_P + k * phi_Q
        phi = E.isogeny(S, algorithm="factored")
        return phi.codomain().j_invariant()


class Participant:
    def __init__(self, sidh: SIDHKeyExchange, k=None):
        self.sidh = sidh
        self.k = k if k else random.randint(0, sidh.n - 1)
        self.public_key = None
        self.P = None
        self.Q = None
        self.P_other = None
        self.Q_other = None
        self.shared_secret = None

    def generate_public_key(self):
        self.public_key = self.sidh.gen_public_key(self.P, self.Q, self.P_other, self.Q_other, self.k)

    def compute_shared_secret(self, other_public_key):
        E, phi_P, phi_Q = other_public_key
        self.shared_secret = self.sidh.get_secret(E, phi_P, phi_Q, self.k)

    def encrypt_message(self, message):
        key = SHA256.new(data=str(self.shared_secret).encode()).digest()
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(message, 16))

        return iv.hex(), ct.hex()

class Server(Participant):
    def __init__(self, sidh: SIDHKeyExchange, k=None):
        super().__init__(sidh, k)
        self.P = (sidh.n // 2**sidh.ea) * sidh.P
        self.Q = (sidh.n // 2**sidh.ea) * sidh.Q
        self.P_other = (sidh.n // 3**sidh.eb) * sidh.P
        self.Q_other = (sidh.n // 3**sidh.eb) * sidh.Q


# params
ea, eb = 216, 137
Px, Py = "19629002260899253283957946747466897522475660429050952494632348990720012643804186952501717429174343892395039800185878841093698753933*i + 21000588886550169078507395472843540543638380042132530088238158553508923414317518502680121549885061095065934470295106985227640283273", "13560249428793295825208984866590149450862696800181907880173464654955696194787095135464283707858591438577968786063706580965498135934*i + 21227525746542853125364742330159420698250203945016980815891234503309307307571119288025866772923240030378597416196914652205098993851"
Qx, Qy = "20653307324266777301745266224745462280019066788351952077152874786877832545975431386178311539432979313717724415603792104905464166613*i + 23543412524221765729252528306934564386341553623491347201198996167100895162007001691940922919130176638905146054229833255452149631903", "20303099683704256985792197307242241000101523982229217515269602102967877919445169730337445309155396940855065338113695974349986136276*i + 18114250244485018537853099412437907124848306019791525046747068726333108423955919092536186121751860512435214970727124588973589483061"

sidh = SIDHKeyExchange(ea, eb, Px, Py, Qx, Qy)

server = Server(sidh, k)

server.generate_public_key()

E, phi_P, phi_Q = server.public_key

print("Server public key")
print("E")
print(f"Ea4: {E.a4()}")
print(f"Ea6: {E.a6()}")
print("phi_P")
print(f"x: {phi_P[0]}")
print(f"y: {phi_P[1]}")
print("phi_Q")
print(f"x: {phi_Q[0]}")
print(f"y: {phi_Q[1]}")

print()
print("Input your public key")
print("Input elliptic curve")
Ea4 = input("Ea4: ")
Ea6 = input("Ea6: ")
E = EllipticCurve(sidh.F, [Ea4, Ea6])

print("Input phi_P")
x = input("x: ")
y = input("y: ")
phi_P = E(x, y)
print("Input phi_Q")
x = input("x: ")
y = input("y: ")
phi_Q = E(x, y)

other_public_key = (E, phi_P, phi_Q)
server.compute_shared_secret(other_public_key)

iv, ct = server.encrypt_message(secret_message)

print("Encrypted message")
print(f"iv: {iv}")
print(f"ct: {ct}")
