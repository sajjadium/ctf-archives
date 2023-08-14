import random as rnd
import logging
import re
import socketserver
from hashlib import blake2b
from Crypto.Cipher import AES
from gmpy2 import isqrt
from py_ecc.fields import optimized_bn128_FQ
from py_ecc.optimized_bn128.optimized_curve import (
    Optimized_Point3D,
    normalize,
    G1,
    multiply,
    curve_order,
    add,
    neg,
)
from flag import flag

hello_string = """Hello, adventurer! A wise sage told me that you can predict the future. Let's see if you can predict my private key. Shhhhhhhh! Send it securely
"""
help_string = """
Usage:
ecdh <(x,y)> - send the point to establish an ECDH tunnel
answer <hex> - send the answer to the question "What is my private key?" encrypted in hex from
help - this info
"""
prompt = ">"


def egcd_step(prev_row, current_row):
    (s0, t0, r0) = prev_row
    (s1, t1, r1) = current_row
    q_i = r0 // r1
    return (s0 - q_i * s1, t0 - q_i * t1, r0 - q_i * r1)


def find_decomposers(lmbda, modulus):
    mod_root = isqrt(modulus)

    egcd_trace = [(1, 0, modulus), (0, 1, lmbda)]
    while egcd_trace[-2][2] >= mod_root:
        egcd_trace.append(egcd_step(egcd_trace[-2], egcd_trace[-1]))

    (_, t_l, r_l) = egcd_trace[-3]
    (_, t_l_plus_1, r_l_plus_1) = egcd_trace[-2]
    (_, t_l_plus_2, r_l_plus_2) = egcd_trace[-1]
    (a_1, b_1) = (r_l_plus_1, -t_l_plus_1)
    if (r_l**2 + t_l**2) <= (r_l_plus_2**2 + t_l_plus_2**2):
        (a_2, b_2) = (r_l, -t_l)
    else:
        (a_2, b_2) = (r_l_plus_2, -t_l_plus_2)

    return (a_1, b_1, a_2, b_2)


lmbda = 4407920970296243842393367215006156084916469457145843978461
beta = 2203960485148121921418603742825762020974279258880205651966

(a_1, b_1, a_2, b_2) = find_decomposers(lmbda, curve_order)


def compute_balanced_representation(scalar, modulus):
    c_1 = (b_2 * scalar) // modulus
    c_2 = (-b_1 * scalar) // modulus
    k_1 = scalar - c_1 * a_1 - c_2 * a_2
    k_2 = -c_1 * b_1 - c_2 * b_2
    return (k_1, k_2)


def multiply_with_endomorphism(x: int, y: int, scalar: int):
    assert scalar >= 0 and scalar < curve_order
    point = (optimized_bn128_FQ(x), optimized_bn128_FQ(y), optimized_bn128_FQ.one())
    endo_point = (
        optimized_bn128_FQ(x) * optimized_bn128_FQ(beta),
        optimized_bn128_FQ(y),
        optimized_bn128_FQ.one(),
    )
    (k1, k2) = compute_balanced_representation(scalar, curve_order)
    print("K decomposed:", k1, k2)
    if k1 < 0:
        point = neg(point)
        k1 = -k1
    if k2 < 0:
        endo_point = neg(endo_point)
        k2 = -k2
    return normalize(add(multiply(point, k1), multiply(endo_point, k2)))


(HOST, PORT) = ("0.0.0.0", 1337)


class CheckHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # Generate the private key
        private_key = rnd.randint(2, curve_order - 1)
        print("Private key:", private_key)
        public_key = multiply_with_endomorphism(G1[0].n, G1[1].n, private_key)
        self.request.sendall((hello_string + help_string + prompt).encode())
        session_key = normalize(G1)
        while True:
            # self.request is the TCP socket connected to the client
            try:
                data = self.request.recv(2048).strip().decode()
                (command, arguments) = data.split(" ")
                if command == "help":
                    self.request.sendall((help_string + prompt).encode())
                elif command == "ecdh":
                    (p_x, p_y) = map(
                        int,
                        re.match(
                            r"\((\d+),(\d+)\)", "".join(arguments).replace(" ", "")
                        )
                        .group()[1:-1]
                        .split(","),
                    )
                    session_key = multiply_with_endomorphism(p_x, p_y, private_key)
                    print(session_key)
                    hash_check = blake2b((str(session_key) + "0").encode()).hexdigest()
                    self.request.sendall(
                        (
                            f"Public key: {str(public_key)}, session check: {hash_check}\n"
                            + prompt
                        ).encode()
                    )
                elif command == "answer":
                    fct = bytes.fromhex("".join(arguments))
                    if len(fct) < 32:
                        self.request.sendall(("IV + CT too short" + prompt).encode())
                        continue
                    key = blake2b((str(session_key) + "1").encode()).digest()[
                        : AES.key_size[-1]
                    ]
                    aes = AES.new(key, AES.MODE_CBC, fct[: AES.block_size])
                    pt = aes.decrypt(fct[AES.block_size :])
                    answer = int(pt.decode())
                    if answer == private_key:
                        self.request.sendall(f"Yay! Here is your flag: {flag}".encode())
                        return
                    else:
                        self.request.sendall("No, wrong answer".encode())
                        return

            except ValueError:
                logging.error("Conversion problem or bad data")
                self.request.sendall(("Malformed data\n" + prompt).encode())
                continue
            except ConnectionResetError:
                logging.error("Connection reset by client")
                return
            except UnicodeDecodeError:
                logging.error("Client sent weird data")
                return
            except AttributeError:
                logging.error("Malformed command")
                self.request.sendall(("Malformed command\n" + prompt).encode())
                continue


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename="server.log",
        filemode="w",
    )
    server = socketserver.TCPServer((HOST, PORT), CheckHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    logging.info(f"Started listenning on {HOST}:{PORT}")
    server.serve_forever()
