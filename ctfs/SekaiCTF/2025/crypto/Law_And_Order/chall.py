from py_ecc.secp256k1 import P, G as G_lib, N
from py_ecc.secp256k1.secp256k1 import multiply, add
import random
import os
from hashlib import sha256
import sys

CONTEXT = os.urandom(69)
NUM_PARTIES = 9
THRESHOLD = (2 * NUM_PARTIES) // 3 + 1
NUM_SIGNS = 100
FLAG = os.environ.get("FLAG", "FLAG{I_AM_A_NINCOMPOOP}")

# IO
def send(msg):
    print(msg, flush=True)


def handle_error(msg):
    send(msg)
    sys.exit(1)


def receive_line():
    try:
        return sys.stdin.readline().strip()
    except BaseException:
        handle_error("Connection closed by client. Exiting.")


def input_int(range=P):
    try:
        x = int(receive_line())
        assert 0 <= x <= range - 1
        return x
    except BaseException:
        handle_error("Invalid input integer")


def input_point():
    try:
        x = input_int()
        y = input_int()
        assert not (x == 0 and y == 0)
        return Point(x, y)
    except BaseException:
        handle_error("Invalid input Point")


# Helper class
class Point:
    """easy operator overloading"""

    def __init__(self, x, y):
        self.point = (x, y)

    def __add__(self, other):
        return Point(*add(self.point, other.point))

    def __mul__(self, scalar):
        return Point(*multiply(self.point, scalar))

    def __rmul__(self, scalar):
        return Point(*multiply(self.point, scalar))

    def __neg__(self):
        return Point(self.point[0], -self.point[1])

    def __eq__(self, other):
        return (self + (-other)).point[0] == 0

    def __repr__(self):
        return str(self.point)


G = Point(*G_lib)


def random_element(P):
    return random.randint(1, P - 1)


def H(*args):
    return int.from_bytes(sha256(str(args).encode()).digest(), "big")


def sum_pts(points):
    res = 0 * G
    for point in points:
        res = res + point
    return res


def sample_poly(t):
    return [random_element(N) for _ in range(t)]


def gen_proof(secret, i):
    k = random_element(P)
    R = k * G
    mu = k + secret * H(CONTEXT, i, secret * G, R)
    return R, mu % N


def verify_proof(C, R, mu, i):
    c = H(CONTEXT, i, C, R)
    return R == mu * G + (-c * C)


def gen_poly_comms(coeffs):
    return [i * G for i in coeffs]


def eval_poly(coeffs, x):
    res = 0
    for coeff in coeffs[::-1]:
        res = (res * x + coeff) % N
    return res


def gen_shares(n, coeffs):
    return {i: eval_poly(coeffs, i) for i in range(1, n + 1)}


def poly_eval_comms(comms, i):
    return sum_pts([comms[k] * pow(i, k, N) for k in range(THRESHOLD)])


def check_shares(comms, shares, i):
    return G * shares[i] == poly_eval_comms(comms, i)


def gen_nonsense():
    d, e = random_element(N), random_element(N)
    D, E = d * G, e * G
    return (d, e), (D, E)


def lamb(i, S):
    num, den = 1, 1
    for j in S:
        if j == i:
            continue
        num *= j
        den *= (j - i)
    return (num * pow(den, -1, N)) % N


def main():
    """https://eprint.iacr.org/2020/852.pdf"""
    send("=" * 50)
    send("=== Law and Order! You should always include your friends to sign and you are mine <3 ===")
    send("=" * 50)
    send( f"We have {NUM_PARTIES - 1} parties here, and you will be party #{NUM_PARTIES}.")
    send(f"Idk why is our group signing not working")
    send("\n--- Round 1: Commitment ---")

    # Keygen

    send(f"context string {CONTEXT.hex()}")

    your_id = NUM_PARTIES

    all_coeffs = {}
    all_comms = {}
    for i in range(1, NUM_PARTIES):
        # 1.1
        coeffs = sample_poly(THRESHOLD)
        # 1.2
        zero_proof = gen_proof(coeffs[0], i)
        # 1.3
        comms = gen_poly_comms(coeffs)
        # 1.5
        if not verify_proof(comms[0], zero_proof[0], zero_proof[1], i):
            handle_error(f"[-] Party {i} secret PoK invalid")
        all_coeffs[i] = coeffs
        all_comms[i] = comms
        send(f"[+] Commitments from party {i}:")
        for k, C_ik in enumerate(comms):
            send(f"  C_{i},{k} = {C_ik}")

    send("\n[?] Now, provide the commitments (points) for your coefficients.")
    your_comms = [input_point() for _ in range(THRESHOLD)]
    send("\n[?] Finally, provide your proof-of-knowledge for your secret share (c_i,0).")
    send("[>] Send Point R:")
    your_zero_proof_R = input_point()
    send("[>] Send mu:")
    your_zero_proof_mu = input_int()
    your_zero_proof = (your_zero_proof_R, your_zero_proof_mu)

    if not verify_proof(your_comms[0], your_zero_proof[0], your_zero_proof[1], your_id):
        handle_error(f"[-] party {your_id} secret PoK invalid")
    all_comms[your_id] = your_comms
    send("[+] Your commitments and proof have been accepted.")
    send("\n--- Round 2: Share Distribution ---")

    send(f"[?] Please provide your shares for the other {NUM_PARTIES} parties.")
    # 2.1
    your_shares = {}
    for i in range(1, NUM_PARTIES + 1):
        send(f"[>] Send share for party {i}:")
        your_shares[i] = input_int(N)

    # 2.2
    for i in range(1, NUM_PARTIES + 1):
        if not check_shares(your_comms, your_shares, i):
            handle_error(f"[-] party {your_id} shares for party {i} invalid")
    send("[+] Your shares have been verified")

    all_shares = {}
    for l in range(1, NUM_PARTIES):
        shares_l = gen_shares(NUM_PARTIES, all_coeffs[l])
        for i in range(1, NUM_PARTIES + 1):
            if not check_shares(all_comms[l], shares_l, i):
                handle_error(f"[-] party {l} shares for party {i} invalid")
        all_shares[l] = shares_l
        send(f"[+] Share for you from party {l}: {shares_l[your_id]}")
    all_shares[your_id] = your_shares

    # 2.3
    signing_shares = {}
    for i in range(1, NUM_PARTIES + 1):
        signing_shares[i] = 0
        for j in range(1, NUM_PARTIES + 1):
            signing_shares[i] += all_shares[j][i]

    # 2.4
    group_public_key = sum_pts([all_comms[i][0] for i in range(1, NUM_PARTIES + 1)])
    send(f"\n[+] Group Public Key: {group_public_key}")

    public_shares = {i: v * G for i, v in signing_shares.items()}
    your_public_share = sum_pts([poly_eval_comms(all_comms[j], your_id) for j in range(1, NUM_PARTIES + 1)])
    public_shares[your_id] = your_public_share
    send("[+] Public verification shares have been computed.")

    send(f"\n--- Phase 3: Presign and Sign ({NUM_SIGNS} rounds) ---")
    for _ in range(NUM_SIGNS):
        # presign
        send("[?] Provide your nonces (D_i, E_i) for this round.")
        your_D = input_point()
        your_E = input_point()
        your_nonsense = (your_D, your_E)

        nonsense_sec, nonsense = {}, {}
        for i in range(1, NUM_PARTIES + 1):
            # 1.a, 1.b & 1.c
            (d, e), (D, E) = gen_nonsense()
            nonsense_sec[i] = (d, e)
            nonsense[i] = (D, E)
        nonsense[your_id] = your_nonsense

        # Sign

        # S is set of alpha, alpha is in t to n right?
        S = {random.randint(THRESHOLD, NUM_PARTIES) for _ in range(NUM_PARTIES - THRESHOLD)}
        S.add(your_id)  # should always include you <3
        send(f"[+] Set of signers for this round: {S}")

        m = "GIVE ME THE FLAG PLEASE"
        combined_nonsense = {}

        group_nonsense = 0 * G
        nonsense = {i: nonsense[i] for i in S}
        # 2
        nonsense_ordered = sorted([(i, Di, Ei) for i, (Di, Ei) in nonsense.items()])
        # 4
        rhos = {i: H(i, m, nonsense_ordered) for i in S}
        for i, (D, E) in nonsense.items():
            send(f"[+] Party {i} nonces: D={D}, E={E}")
            D, E = nonsense[i]
            nonsense_i = D + rhos[i] * E
            group_nonsense = group_nonsense + nonsense_i
            combined_nonsense[i] = nonsense_i

        group_challenge = H(group_nonsense, group_public_key, m)
        send(f"[+] Group challenge `c`: {group_challenge}")
        send("[?] Provide your signature share `z_i`.")

        your_zi = input_int(N)

        # 7.b
        if your_zi * G != combined_nonsense[your_id] + \
                public_shares[your_id] * group_challenge * lamb(your_id, S):
            handle_error(f"[-] party {your_id} signature shares invalid")

        final_signing_shares = {your_id: your_zi}
        for i in S - {your_id}:
            si = signing_shares[i]
            di, ei = nonsense_sec[i]
            # 5
            zi = di + (ei * rhos[i]) + si * group_challenge * lamb(i, S)
            Ri, Yi = combined_nonsense[i], public_shares[i]
            if Yi != sum_pts([poly_eval_comms(all_comms[j], i) for j in range(1, NUM_PARTIES + 1)]):
                handle_error(f"[-] party {i} public share invalid")
            if zi * G != Ri + Yi * group_challenge * lamb(i, S):
                handle_error(f"[-] party {i} signature share invalid")
            final_signing_shares[i] = zi

        # 7.c
        z = sum(final_signing_shares.values()) % N

        if z * G == group_nonsense + group_public_key * group_challenge:
            send("[+] Signature verification successful")
            send(f"[+] Here is your flag: {FLAG}")
            sys.exit(0)
    handle_error("[-] We are out of signing ink")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        handle_error("[-] An error occured: {e}")
