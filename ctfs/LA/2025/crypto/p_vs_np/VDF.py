# Inspired by https://github.com/BqETH/PietrzakVDF/blob/main/PietrzakVDF.py
import binascii
import math
import hashlib
import time

def r_value(x, y, μ, int_size_bits=1024):
    """Generates the Fiat-Shamir verifier challenges Hash(xi,yi,μi)"""
    int_size = int_size_bits // 8
    s = (x.to_bytes(int_size, "big", signed=False) +
         y.to_bytes(int_size, "big", signed=False) +
         μ.to_bytes(int_size, "big", signed=False))
    b = hashlib.sha256(s).digest()
    return int.from_bytes(b[:16], "big")

def generate_proof(xi, t, δ, yi, N, i, π=[]):
    """  Generate the proof, list of μi values """
    # Halving protocol from Pietrzak p16.
    # μi = xi^(2^(T/2^i))
    # ri = Hash((xi,T/2^(i−1),yi),μi)
    # xi+1 = xi^ri . μi
    # yi+1 = μi^ri . yi

    t = t//2  # or t = int(τ / pow(2, i))
    μi = pow(xi, pow(2, t), N)
    ri = r_value(xi, yi, μi) % N
    xi = (pow(xi, ri, N) * μi) % N
    yi = (pow(μi, ri, N) * yi) % N
    π.append(μi)
    print("Values: T:{}, x{}:{}, y{}:{}, u{}:{}, r{}: {}".format(t, i, xi, i, yi, i, μi, i, ri))

    # Verify we can build a proof for the leaf
    if t == pow(2, δ):
        xi_delta = pow(xi, pow(2, pow(2, δ)), N)
        if xi_delta == yi:
            print("Match Last (x{})^2^2^{} {} = y{}: {}".format(i, δ, xi_delta, i, yi))
            return π
        else:
            print("Proof incomplete.")
            return

    return generate_proof(xi, t, δ, yi, N, i+1, π)

def repeated_squarings(N, x, τ):
    """ Repeatedly square x. """
    return pow(x, pow(2, τ), N)

def basic_proof(N, x, τ, δ, s):
    # Compute x^(2^τ) mod N
    y = repeated_squarings(N, x, τ)
    π = generate_proof(x, τ, δ, y, N, 1)
    return y, π

def verify_proof(xi, yi, π, τ, δ, N):
    """ Verify proof """
    # Verify algo from Pietrzak p16.
    # ri := hash((xi,T/^2i−1,yi), μi)
    # xi+1 := xi^ri . μi
    # yi+1 := μi^ri . yi
    while(len(π) != 0):
        μi = π.pop()
        ri = r_value(xi, yi, μi) % N
        xi = (pow(xi, ri, N) * μi) % N
        yi = (pow(μi, ri, N) * yi) % N
        # yt+1 ?= (xt+1)^2
    if yi == pow(xi,pow(2, pow(2, δ)),N):
        return True
    else:
        return False



if __name__ == '__main__':
    print('This illustrates the Pietrzak VDF unoptimized proving.')
    # primes.rwh_primes1(123456789123456789)
    # Pick two of them.
    p = 123456211
    q = 123384263
    # p,q Need to be safe primes. p = 2p′+1 and q = 2q′ +1
    # i.e. p′ = (p −1)/2 and q′ = (q −1)/2  also prime


    # t is the number of bits in τ=2^t
    t = 25
    # Tau
    τ = pow(2, t)
    # Prime Composite N
    N = p * q

    # Some Random value X
    x = pow(509, 23) % N

    print("Values: p:{},q:{} -> N:{}".format(p, q, N))
    print("Values: t:{} -> τ:{}, x:{}".format(t, τ, x))

    # Malicious Solver's VDF takes a while
    start_t = time.time() * 1000
    y = pow(x, pow(2, τ), N) % N
    print("Values: y:{}".format(y))
    print("Finished y in ", round(((time.time() * 1000) - start_t), 2), "ms")

    # Honest Prover's VDF takes even longer
    start_t = time.time() * 1000
    # Using a δ value makes the verification require a costly xi ^ pow(2,pow(2,δ)) but shortens the proof
    δ = 0
    s = 0
    print("Delta: δ:{}".format(δ))
    y, π = basic_proof(N, x, τ, δ, s)
    print("length of pi", len(π))
    print("Finished total calc+proof in ", round(((time.time() * 1000) - start_t), 2), "ms")
    # Output the proof
    print("Result:", y)
    # Should π=[μi] have Log2(T) elements minus the delta optimization.
    print("Proof:", π)

    # Proof Verification
    start_t = time.time() * 1000
    ok = verify_proof(x, y, π, τ, δ,N)
    if ok:
        print("Proof is valid. Finished verifying in ", round(((time.time() * 1000) - start_t), 2), "ms")
