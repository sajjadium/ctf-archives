#!/usr/bin/env python3

"""
Code from https://github.com/NikolaiT/Dragonfly-SAE/blob/master/dragonfly_implementation.py

"""
import time
import hashlib
import hmac
import secrets
import logging
from collections import namedtuple
import socket
import struct
import random
import os
import signal
import string
import secrets

logger = logging.getLogger('dragonfly')
logger.setLevel(logging.INFO)


Point = namedtuple("Point", "x y")
# The point at infinity (origin for the group law).
O = 'Origin'

def lsb(x):
    binary = bin(x).lstrip('0b')
    return binary[0]

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(n, p):
    """
    # https://rosettacode.org/wiki/Tonelli-Shanks_algorithm#Python
    """
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def hmac_sha256(key, msg):
    h = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return h.digest()


class Curve():
    """
    Mathematical operations on a Elliptic Curve.

    A lot of code taken from:
    https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python
    """

    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.defense_masks = []
        self.dN = 100
        for i in range(self.dN):
            self.defense_masks += [secrets.randbelow(self.p-1) + 1]

    def curve_equation(self, x):
        """
        We currently use the elliptic curve
        NIST P-384
        """
        return (pow(x, 3) + (self.a * x) + self.b) % self.p

    def secure_curve_equation(self, x):
        """
        Do not leak hamming weights to power analysis
        """
        idx = secrets.randbelow(self.dN)
        defense = self.defense_masks + []
        defense[idx] = x
        for i in range(self.dN):
            tmp = defense[idx]
            defense[i] = self.curve_equation(defense[idx])
        return defense[idx]

    def is_quadratic_residue(self, x):
        """
        https://en.wikipedia.org/wiki/Euler%27s_criterion
        Computes Legendre Symbol.
        """
        return pow(x, (self.p-1) // 2, self.p) == 1

    def secure_is_quadratic_residue(self, x):
        """
        Do not leak hamming weights to power analysis
        """
        idx = secrets.randbelow(self.dN)
        defense = self.defense_masks + []
        defense[idx] = x
        for i in range(self.dN):
            defense[i] = self.is_quadratic_residue(defense[i])
        return defense[idx]

    def valid(self, P):
        """
        Determine whether we have a valid representation of a point
        on our curve.  We assume that the x and y coordinates
        are always reduced modulo p, so that we can compare
        two points for equality with a simple ==.
        """
        if P == O:
            return True
        else:
            return (
                (P.y**2 - (P.x**3 + self.a*P.x + self.b)) % self.p == 0 and
                0 <= P.x < self.p and 0 <= P.y < self.p)

    def inv_mod_p(self, x):
        """
        Compute an inverse for x modulo p, assuming that x
        is not divisible by p.
        """
        if x % self.p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.p-2, self.p)

    def ec_inv(self, P):
        """
        Inverse of the point P on the elliptic curve y^2 = x^3 + ax + b.
        """
        if P == O:
            return P
        return Point(P.x, (-P.y) % self.p)

    def ec_add(self, P, Q):
        """
        Sum of the points P and Q on the elliptic curve y^2 = x^3 + ax + b.
        https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python
        """
        if not (self.valid(P) and self.valid(Q)):
            raise ValueError("Invalid inputs")

        # Deal with the special cases where either P, Q, or P + Q is
        # the origin.
        if P == O:
            result = Q
        elif Q == O:
            result = P
        elif Q == self.ec_inv(P):
            result = O
        else:
            # Cases not involving the origin.
            if P == Q:
                dydx = (3 * P.x**2 + self.a) * self.inv_mod_p(2 * P.y)
            else:
                dydx = (Q.y - P.y) * self.inv_mod_p(Q.x - P.x)
            x = (dydx**2 - P.x - Q.x) % self.p
            y = (dydx * (P.x - x) - P.y) % self.p
            result = Point(x, y)

        # The above computations *should* have given us another point
        # on the curve.
        assert self.valid(result)
        return result

    def double_add_algorithm(self, scalar, P):
        """
        Double-and-Add Algorithm for Point Multiplication
        Input: A scalar in the range 0-p and a point on the elliptic curve P
        https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python
        """
        assert self.valid(P)

        b = bin(scalar).lstrip('0b')
        T = P
        for i in b[1:]:
            T = self.ec_add(T, T)
            if i == '1':
                T = self.ec_add(T, P)

        assert self.valid(T)
        return T

class Peer:
    """
    Implements https://wlan1nde.wordpress.com/2018/09/14/wpa3-improving-your-wlan-security/
    Take a ECC curve from here: https://safecurves.cr.yp.to/

    Example: NIST P-384
    y^2 = x^3-3x+27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575
    modulo p = 2^384 - 2^128 - 2^96 + 2^32 - 1
    2000 NIST; also in SEC 2 and NSA Suite B

    See here: https://www.rfc-editor.org/rfc/rfc5639.txt

   Curve-ID: brainpoolP256r1
      p =
      A9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377
      A =
      7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9
      B =
      26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6
      x =
      8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262
      y =
      547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997
      q =
      A9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7
      h = 1
    """

    def __init__(self, password, mac_address, name):
        self.name = name
        self.password = password
        self.mac_address = mac_address

        # Try out Curve-ID: brainpoolP256t1
        self.p = int('A9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377', 16)
        self.a = int('7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9', 16)
        self.b = int('26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6', 16)
        self.q = int('A9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7', 16)
        self.curve = Curve(self.a, self.b, self.p)

    def initiate(self, other_mac, k=40):
        """
        See algorithm in https://tools.ietf.org/html/rfc7664
        in section 3.2.1
        """
        self.other_mac = other_mac
        found = 0
        num_valid_points = 0
        counter = 1
        n = self.p.bit_length()

        # Find x
        while counter <= k:
            base = self.compute_hashed_password(counter)
            temp = self.key_derivation_function(n, base, b'Dragonfly Hunting And Pecking')
            if temp >= self.p:
                counter = counter + 1
                continue
            seed = temp
            val = self.curve.secure_curve_equation(seed)
            if self.curve.secure_is_quadratic_residue(val):
                if num_valid_points < 5:
                    x = seed
                    save = base
                    found = 1
                    num_valid_points += 1
                    logger.debug('Got point after {} iterations'.format(counter))

            counter = counter + 1

        if found == 0:
            logger.error('No valid point found after {} iterations'.format(k))
            return False
        elif found == 1:
            # https://crypto.stackexchange.com/questions/6777/how-to-calculate-y-value-from-yy-mod-prime-efficiently
            # https://rosettacode.org/wiki/Tonelli-Shanks_algorithm
            y = tonelli_shanks(self.curve.curve_equation(x), self.p)

            PE = Point(x, y)

            # check valid point
            assert self.curve.curve_equation(x) == pow(y, 2, self.p)

            self.PE = PE
            assert self.curve.valid(self.PE)
            return True

    def commit_exchange(self):
        self.private = secrets.randbelow(self.p-1) + 1
        self.mask = secrets.randbelow(self.p-1) + 1

        self.scalar = (self.private + self.mask) % self.q

        if self.scalar < 2:
            raise ValueError('Scalar is {}, regenerating...'.format(self.scalar))

        P = self.curve.double_add_algorithm(self.mask, self.PE)
        self.element = self.curve.ec_inv(P)

        assert self.curve.valid(self.element)
        return self.scalar, self.element

    def compute_shared_secret(self, peer_element, peer_scalar, peer_mac):
        self.peer_element = peer_element
        self.peer_scalar = peer_scalar
        self.peer_mac = peer_mac

        assert self.curve.valid(self.peer_element)

        # If both the peer-scalar and Peer-Element are
        # valid, they are used with the Password Element to derive a shared
        # secret, ss:

        Z = self.curve.double_add_algorithm(self.peer_scalar, self.PE)
        ZZ = self.curve.ec_add(self.peer_element, Z)
        K = self.curve.double_add_algorithm(self.private, ZZ)

        self.k = K[0]

        own_message = '{}{}{}{}{}{}'.format(self.k , self.scalar , self.peer_scalar , self.element[0] , self.peer_element[0] , self.mac_address).encode()

        H = hashlib.sha256()
        H.update(own_message)
        self.token = H.hexdigest()
        return self.token

    def confirm_exchange(self, peer_token):
        peer_message = '{}{}{}{}{}{}'.format(self.k , self.peer_scalar , self.scalar , self.peer_element[0] , self.element[0] , self.peer_mac).encode()
        H = hashlib.sha256()
        H.update(peer_message)
        self.peer_token_computed = H.hexdigest()

        #print('[{}] Computed Token from Peer={}'.format(self.name, self.peer_token_computed))
        #print('[{}] Received Token from Peer={}'.format(self.name, peer_token))

        if peer_token != self.peer_token_computed:
            return False

        # Pairwise Master Key” (PMK)
        # compute PMK = H(k | scal(AP1) + scal(AP2) mod q)
        pmk_message = '{}{}'.format(self.k, (self.scalar + self.peer_scalar) % self.q).encode()
        H = hashlib.sha256()
        H.update(pmk_message)
        self.PMK = H.hexdigest()

        logger.info('[{}] Pairwise Master Key(PMK)={}'.format(self.name, self.PMK))
        return True

    def key_derivation_function(self, n, base, seed):
        """
        B.5.1 Per-Message Secret Number Generation Using Extra Random Bits

        Key derivation function from Section B.5.1 of [FIPS186-4]

        The key derivation function, KDF, is used to produce a
        bitstream whose length is equal to the length of the prime from the
        group's domain parameter set plus the constant sixty-four (64) to
        derive a temporary value, and the temporary value is modularly
        reduced to produce a seed.
        """
        combined_seed = '{}{}'.format(base, seed).encode()

        # base and seed concatenated are the input to the RGB
        random.seed(combined_seed)

        # Obtain a string of N+64 returned_bits from an RBG with a security strength of
        # requested_security_strength or more.

        randbits = random.getrandbits(n)
        binary_repr = format(randbits, '0{}b'.format(n))

        assert len(binary_repr) == n

        logger.debug('Rand={}'.format(binary_repr))

        # Convert returned_bits to the non-negative integer c (see Appendix C.2.1).
        C = 0
        for i in range(n):
            if int(binary_repr[i]) == 1:
                C += pow(2, n-i)

        logger.debug('C={}'.format(C))

        #k = (C % (n - 1)) + 1

        k = C

        logger.debug('k={}'.format(k))
        return k


    def compute_hashed_password(self, counter):
        maxm = max(self.mac_address, self.other_mac)
        minm = min(self.mac_address, self.other_mac)
        message = '{}{}{}{}'.format(maxm, minm, self.password, counter).encode()
        logger.debug('Message to hash is: {}'.format(message))
        H = hashlib.sha256()
        H.update(message)
        digest = H.digest()
        return digest


def receive_sta_mac(conn):
    data = conn.recv(1024).decode().strip()
    return data

def receive_sta_token(conn):
    data = conn.recv(1024).decode().strip()
    return data

def receive_sta_scalar_element(conn, p):
    data = conn.recv(1024).decode().strip()
    if data.count(",") != 2:
        return 0, 0
    scalar_sta, element_sta_x, element_sta_y = data.split(',')

    if int(scalar_sta) < 2 or int(element_sta_x) < 2 or int(element_sta_y) < 2:
        return 0, 0

    if int(scalar_sta) >= p -1 or int(element_sta_x) >= p - 1 or int(element_sta_y) >= p - 1:
        return 0, 0

    scalar_sta = int(scalar_sta)
    element_sta = Point(int(element_sta_x), int(element_sta_y))
    return scalar_sta, element_sta

def send_sta(conn, message):
    conn.sendall(message.encode())

def sae_state_machine(conn, real_psk, ap_mac):
    state = 0
    mac2 = ap_mac
    max_retries = 0
    ap = Peer(real_psk, mac2, 'AP')

    scalar_sta, element_sta = None, None
    mac1 = None
    sta_token = None

    while True:
        if state == 0:
            send_sta(conn, "I am MAC %s, what is your MAC? " % ap_mac)
            mac1 = receive_sta_mac(conn)
            state = 1
        elif state == 1:
            #logger.info('Starting hunting and pecking to derive PE...\n')
            scalar_ap, element_ap = None, None
            ap.initiate(mac1)
            scalar_ap, element_ap = ap.commit_exchange()
            send_sta(conn, ','.join(map(str, [scalar_ap, element_ap.x, element_ap.y])) + '\n')
            state = 2
        elif state == 2:
            #logger.info('Computing shared secret...\n')
            scalar_sta, element_sta = receive_sta_scalar_element(conn, ap.p)
            if scalar_sta == 0:
                #reset state
                state = 0
                continue
            ap_token = ap.compute_shared_secret(element_sta, scalar_sta, mac1)
            state = 3
        elif state == 3:
            #logger.info('Confirm Exchange...\n')
            send_sta(conn, "Token? ")
            sta_token = receive_sta_token(conn)
            if ap.confirm_exchange(sta_token) == True:
                d=open("flag.txt").read()
                send_sta(conn, d+"\n")
                send_sta(conn, "FLAG WAS SENT\n")
                exit(0)
            else:
                send_sta(conn, "you didnt solve...\n")
                if max_retries >= 2:
                    send_sta(conn, "[!] HACKING FAIL DETECTED [!]\n")
                    exit(1)
                max_retries += 1


def gen_password():
    characters = string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(5))
    return password

def main():
    host = '0.0.0.0'
    port = 2561
    max_clients = 20

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(max_clients)


        client_count = 0
        while True:
            conn, addr = s.accept()
            pid = os.fork()
            if pid == 0:
                # Child process
                s.close()  # Close the listening socket in the child process
                signal.alarm(300)  # Set the connection time limit to 300 seconds
                print(f"Connected by {addr}")

                real_psk = gen_password()
                print(real_psk)
                ap_mac = '01:02:03:0a:0b:0c'
                sae_state_machine(conn, real_psk, ap_mac)
                conn.close()
                os._exit(0)
            else:
                try:
                  os.waitpid(-1, os.WNOHANG)
                except:
                  pass
                conn.close()

if __name__ == '__main__':
    main()
