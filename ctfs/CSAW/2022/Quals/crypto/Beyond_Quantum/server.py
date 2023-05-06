import numpy as np
import sys
from cipher.cipher import Cipher
from cipher.mathutils import random_poly
from sympy.abc import x
from sympy import ZZ, Poly
import math


def encrypt_command(data, public_key):
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    output = encrypt(public_key, input_arr, bin_output=True)
    output = np.packbits(np.array(output).astype(int)).tobytes().hex()
    return output


def poly_to_bytes(poly):
    res = poly.set_domain(ZZ).all_coeffs()[::-1]
    res = np.packbits(np.array(res).astype(int)).tobytes().hex()
    return bytes.fromhex(res)


def decrypt_command(data, private_key):
    input_arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    output = decrypt(private_key, input_arr, bin_input=True)
    output = np.packbits(np.array(output).astype(int)).tobytes().hex()
    output = bytes.fromhex(output)
    return output


def generate(N, p, q):
    cipher = Cipher(N, p, q)
    cipher.generate_random_keys()
    h = np.array(cipher.h_poly.all_coeffs()[::-1])
    f, f_p = np.array(cipher.f_poly.all_coeffs()[::-1]), np.array(cipher.f_p_poly.all_coeffs()[::-1])
    private_key = {'N': N, 'p': p, 'q': q, 'f': f, 'f_p': f_p}
    public_key = {'N': N, 'p': p, 'q': q, 'h': h}
    return (private_key, public_key)


def encrypt(pub_key, input_arr, bin_output=False):
    global h_poly
    global c_poly

    cipher = Cipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    cipher.h_poly = Poly(pub_key['h'].astype(int)[::-1], x).set_domain(ZZ)
    h_poly = cipher.h_poly

    if cipher.N < len(input_arr):
        raise Exception("Input is too large for current N")

    c_poly = cipher.encrypt(Poly(input_arr[::-1], x).set_domain(ZZ), random_poly(cipher.N, int(math.sqrt(cipher.q))))
    output = c_poly.all_coeffs()[::-1]
    if bin_output:
        k = int(math.log2(cipher.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]

    return np.array(output).flatten()


def decrypt(priv_key, input_arr, bin_input=False):
    cipher = Cipher(int(priv_key['N']), int(priv_key['p']), int(priv_key['q']))
    cipher.f_poly = Poly(priv_key['f'].astype(int)[::-1], x).set_domain(ZZ)
    cipher.f_p_poly = Poly(priv_key['f_p'].astype(int)[::-1], x).set_domain(ZZ)
    if bin_input:
        k = int(math.log2(cipher.q))
        pad = k - len(input_arr) % k
        if pad == k:
            pad = 0
        input_arr = np.array([int("".join(n.astype(str)), 2) for n in
                              np.pad(np.array(input_arr), (0, pad), 'constant').reshape((-1, k))])
    if cipher.N < len(input_arr):
        raise Exception("Input is too large for current N")
    return cipher.decrypt(Poly(input_arr[::-1], x).set_domain(ZZ)).all_coeffs()[::-1]


def get_password():
    with open("password.txt") as file:
        password = "".join(file.readlines()).strip()
    return password


def main():
    password = get_password()

    print("**********      B E Y O N D   Q U A N T U M      **********\n")
    print("   I heard that quantums are flying around these days and")
    print("people are thinking of attacking cryptosystems with them.")
    print("So I found this awesome cryptosystem that is safe from")
    print("quantums! You can send as many qubits as you like at this")
    print("cipher, and none of them will break it. Here is a proof of")
    print("concept to show the world how robust our cryptosystem is.")
    print("I\'ve encrypted a password and no amount of skullduggery")
    print("will help you to get it back. See, you can encrypt and")
    print("decrypt all you want, you won\'t get anywhere!")

    private_key, public_key = generate(N=97, p=3, q=128)
    print("   This is an asymmetric cryptosystem so here is the public")
    print("key:\n")
    print(str(public_key) + "\n")
    pwd_ct = encrypt_command(password.encode(), public_key)
    print("   The password ciphertext is " + pwd_ct + "\n")
    print("   Have at it!\n")

    while True:
        print("/------------------------------\\")
        print("|           COMMANDS           |")
        print("|                              |")
        print("|   1) ciphertext_as_poly         |")
        print("|   2) publickey_as_poly          |")
        print("|   3) solve_challenge <password> |")
        print("|   4) exit                       |")
        print("\\------------------------------/\n")
        print("> ", end="")
        sys.stdout.flush()
        parts = sys.stdin.readline()[:-1].split(" ")

        try:
            if parts[0] == "ciphertext_as_poly" or parts[0] == "1":
                print(c_poly)
                sys.stdout.flush()
            elif parts[0] == "publickey_as_poly" or parts[0] == "2":
                print(h_poly)
                sys.stdout.flush()
            elif parts[0] == "solve_challenge" or parts[0] == "3":
                candidate_password = parts[1]
                if candidate_password == password:
                    print("\nWhat?! How did you do that??\n")
                    with open("flag.txt") as file:
                        print("".join(file.readlines()))
                else:
                    print("\nNope!\n")
            elif parts[0] == "exit" or parts[0] == "4":
                print("\nBye!")
                sys.stdout.flush()
                return
            else:
                print("\nUnknown command.")
                raise Exception()
        except:
            print("\nSomething went wrong...")
            print("...try again?\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
