#!/usr/bin/env sage
import os
import random
import operator
from functools import reduce
from tqdm import tqdm
from sage.structure.coerce_maps import CallableConvertMap
from sage.groups.group_semidirect_product import GroupSemidirectProduct, GroupSemidirectProductElement
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import ChaCha20

FLAG = os.getenv("FLAG", "DUCTF{dummy_flag}").encode("ascii")


class ColouredBurauGroupElement(GroupSemidirectProductElement):
    """
    An element of the coloured Burau group M ⋊ G
    """

    def evaluate(self, codomain):
        """
        Let τ_i be a fixed element of GF(p)^n and φ: M -> N be the evaluation
        map at τ_i. This method applies the map (φ × 1) to `self`. The result is
        coerced into an element of `codomain`
        """

        parent = self.parent()
        M, _ = parent.cartesian_factors()
        t_i = M.base_ring().gens()

        mat, perm = self.cartesian_factors()
        sub_map = {t: tau for t, tau in zip(t_i, parent.tau_i)}
        return codomain((mat.matrix().subs(sub_map), perm))

    def _act_on_(self, x, self_on_left):
        """
        The Algebraic Eraser operation, as a right group action of M ⋊ G on N × G.
        """

        if self_on_left != self.parent().act_to_right():
            raise ValueError("Group action side-mismatch")

        codomain = x.parent()
        x = x.cartesian_factors()
        actor = self.parent()
        return (actor(x) * self).evaluate(codomain)


class ColouredBurauGroup(GroupSemidirectProduct):
    """
    The coloured Burau group M ⋊ G.
    """

    def __init__(self, M, G, tau_i):
        self.M = M
        self.G = G
        self.Element = ColouredBurauGroupElement
        self.tau_i = tau_i
        super().__init__(M, G, twist=self._twist_, print_tuple=True, act_to_right=False)

    def _twist_(self, g, a):
        """
        Applies the twist homomorphism given by the permutation action of G
        on the indeterminates {t_1, ... t_n}.
        """

        t_i = self.M.base_ring().gens()

        sub_map = {t: gt for t, gt in zip(t_i, g(t_i))}
        return a.subs(sub_map)

    def _coerce_map_from_(self, S):
        """
        Extends ``GroupSemidirectProduct` to enable coercion from the Braid
        group on n strands via the coloured Burau representation.
        """

        if S == BraidGroup(self.G.degree()):

            def f(braid_element):
                cb = self._coloured_burau_matrix_(braid_element)
                perm = braid_element.permutation(self.G)
                return self((cb, perm))

            return CallableConvertMap(S, self, f, parent_as_first_arg=False)
        return None

    def gens(self):
        Bn = BraidGroup(self.G.degree())
        return tuple(self(b) for b in Bn.gens())

    def random_element(self, length, gens=None):
        if gens is None:
            gens = self.gens()

        syllables = list(gens) + [b.inverse() for b in gens]
        word = prod(random.choices(syllables, k=length))
        return word

    def _coloured_burau_matrix_(self, braid_element):
        t_i = self.M.base_ring().gens()
        b_i = braid_element.parent().gens()

        accumulator = self.M.one()
        for artin_generator, exponent in braid_element.syllables():
            i = b_i.index(artin_generator)
            coloured_burau = (artin_generator**exponent).burau_matrix(reduced="simple").subs(t=t_i[i])
            accumulator *= coloured_burau

        return accumulator


class AESKey:
    def __init__(self, public, private):
        self.public = public
        self.private = private


class AlgebraicEraserScheme:
    """
    The trusted third party of the Algebraic Eraser scheme.
    """

    def __init__(self, M, N, G):
        self.tau_i = self._generate_tau_(M)
        self.MG = ColouredBurauGroup(M, G, self.tau_i)
        self.NG = N.cartesian_product(G)
        self.kappa = self._generate_kappa_()

        self.A, self.B = self._select_conjugates_()

    def generate(self, party, m=64):
        """
        Generates an AES public + private keypair
        """

        _, G = self.NG.cartesian_factors()
        matrix_perm = self.NG((self._generate_priv_matrix(), G.one()))

        if party == "A":
            braid = random.choices(self.A, k=m)
        elif party == "B":
            braid = random.choices(self.B, k=m)
        else:
            raise ValueError('`party` must be one of "A" or "B"')
        private = (matrix_perm, braid)

        public = reduce(
            operator.mul,
            tqdm(braid, desc=f"Calculating public key for party {party}"),
            matrix_perm,
        )

        return AESKey(public, private)

    def _select_conjugates_(self, t=14, s=64):
        """
        Selects (generators for) a pair of E-commuting submonoids A, B of M ⋊ G.
        """
        b_i = self.MG.gens()
        _, G = self.NG.cartesian_factors()
        n = G.degree()

        L = [b_i[i] for i in list(range(0, (n - 1) // 2))]
        U = [b_i[i] for i in list(range((n - 1) // 2 + 1, n - 1))]

        z = self.MG.random_element(t)

        A, B = (
            [
                z * self.MG.random_element(t, gen) * z.inverse()
                for _ in tqdm(range(s), desc=f"Selecting E-commuting submonoid ({i+1} / 2)")
            ]
            for i, gen in enumerate((L, U))
        )
        return A, B

    def _generate_tau_(self, M):
        """
        Generates τ_i, a fixed element of GF(p)^n
        """
        n = M.base_ring().ngens()
        K = M.base_ring().base_ring()
        while True:
            tau_i = [K.random_element() for _ in range(n)]
            if not any(tau.is_zero() for tau in tau_i):
                return tuple(tau_i)

    def _generate_kappa_(self):
        """
        Generates κ, the seed matrix for client private keys.
        """
        N, _ = self.NG.cartesian_factors()
        while True:
            kappa = N.random_element().matrix()
            if kappa.characteristic_polynomial().is_irreducible():
                return kappa

    def _generate_priv_matrix(self):
        """
        Selects a matrix pseudo-randomly using κ as a seed.
        """
        M = self.MG.M
        n = M.base_ring().ngens()
        K = M.base_ring().base_ring()
        coeffs = [K.random_element() for _ in range(n)]
        return sum(coeffs[i] * self.kappa**i for i in range(n))


def encrypt_flag(shared_secret, flag):
    # Flatten matrix into a reasonable byte-string
    secret_coefficients = shared_secret[0].matrix().change_ring(ZZ).list()
    password = b"".join("{:03x}".format(coeff).encode("ascii") for coeff in secret_coefficients)

    # Derive symmetric key
    salt = b"DownUnderCTF 2024"
    key = PBKDF2(password, salt, 32, count=1000000)

    # Encrypt flag
    nonce = random.randbytes(12)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ct = cipher.encrypt(FLAG)

    return ct, nonce


def publish_exchange_parameters(AES):
    print("tau_i =", AES.tau_i)
    print("kappa =", list(map(list, AES.kappa.rows())))
    print("A =", [(mat.list(), f"{perm}") for mat, perm in AES.A])


def main(n=16, p=743):
    M = GL(n - 1, LaurentPolynomialRing(GF(p), "t", n))
    N = GL(n - 1, GF(p))
    G = SymmetricGroup(n)

    AES = AlgebraicEraserScheme(M, N, G)
    publish_exchange_parameters(AES)

    alice = AES.generate("A")
    bob = AES.generate("B")

    # Alice says:
    print("alice_public_matrix =", alice.public[0].list())
    print(f'alice_public_perm = "{alice.public[1]}"')

    # Bob says:
    print("bob_public_matrix =", bob.public[0].list())
    print(f'bob_public_perm = "{bob.public[1]}"')

    alice_secret = reduce(
        operator.mul,
        tqdm(alice.private[1], desc="Calculating shared secret (A)"),
        alice.private[0] * bob.public,
    )
    bob_secret = reduce(
        operator.mul,
        tqdm(bob.private[1], desc="Calculating shared secret (B)"),
        bob.private[0] * alice.public,
    )

    assert alice_secret == bob_secret

    ct, nonce = encrypt_flag(alice_secret, FLAG)
    print(f'ct = "{ct.hex()}"')
    print(f'nonce = "{nonce.hex()}"')


if __name__ == "__main__":
    main()
