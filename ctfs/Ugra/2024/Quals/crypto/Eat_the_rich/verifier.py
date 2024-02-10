import gmpy2
import random


P = 2 ** 16384 - 364486013  # safe prime


class Verifier:
    def __init__(self):
        self.stage = "nothing"


    def generate(self):
        while True:
            try:
                self.try_generate()
            except AssertionError:
                pass
            else:
                break
        self.stage = "generated_and_want_cs"


    def try_generate(self):
        # y = g^x
        rng = random.Random()
        self.g = rng.getrandbits(16384)
        # g must be a generator
        assert gmpy2.powmod(self.g, (P - 1) // 2, P) != 1
        self.y = rng.getrandbits(16384)
        assert 2 <= self.y < P
        choices = rng.getrandbits(32)
        self.choices = [(choices >> i) & 1 for i in range(32)]


    def prover_announces_cs(self, cs: list[int]):
        # Prover announces proofs, c = g^r mod p
        assert self.stage == "generated_and_want_cs"
        assert len(cs) == len(self.choices)
        for c in cs:
            assert 0 <= c < P
        self.cs = cs
        self.stage = "has_cs_and_want_answers"
        # Verifier asks for (x+r) mod (p-1) or r depending on flag
        return self.choices


    def prover_answers_choices(self, answers: list[int]):
        assert self.stage == "has_cs_and_want_answers"
        assert len(answers) == len(self.choices)
        self.stage = "has_answers"
        for choice, c, answer in zip(self.choices, self.cs, answers):
            assert 0 <= answer < P - 1
            if choice == 0:
                # Verifier asked for (x+r) mod (p-1)
                assert c * self.y % P == gmpy2.powmod(self.g, answer, P)
            else:
                # Verifier asked for r
                assert c == gmpy2.powmod(self.g, answer, P)
