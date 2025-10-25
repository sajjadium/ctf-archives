from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import List, Protocol, Tuple

from openfhe import (
    CCParamsCKKSRNS,
    Ciphertext,
    CryptoContext,
    GenCryptoContext,
    PKESchemeFeature,
    Plaintext,
)

DEBUG_GAME = False


def float_to_bits(value: float, bit_length: int, scale_bits: int) -> Tuple[int, ...]:
    """
    Convert a CKKS plaintext slot to a fixed-length bit tuple.

    Values are first scaled by 2^scale_bits and rounded to the nearest integer.
    The integer is then represented in two's complement with bit_length bits.
    """
    scaled = int(round(value * (1 << scale_bits)))
    scaled = abs(scaled)
    mask = (1 << bit_length) - 1
    twos_complement = scaled & mask
    return tuple((twos_complement >> i) & 1 for i in range(bit_length))


class HomomorphicCKKSFunction(Protocol):
    """Interface for describing circuits usable by the Eval oracle."""

    num_inputs: int

    def plaintext(self, values: Tuple[float, ...]) -> float:
        """Evaluate the circuit on cleartext data."""

    def ciphertext(
        self, cc: CryptoContext, ciphertexts: Tuple[Ciphertext, ...]
    ) -> Ciphertext:
        """Evaluate the same circuit homomorphically on ciphertext inputs."""


@dataclass
class OracleRow:
    """Single row stored by the challenger."""

    m0: float
    m1: float
    ciphertext: Ciphertext


class BitwiseCKKSIndCpaDGame:
    """
    CKKS IND-CPA-D challenger with bit-guarded decryption oracle.

    The challenger maintains a state of tuples (m0, m1, bits0, bits1, Enc(m_b)).
    The decryption oracle reveals Dec(Enc(m_b)) only if the requested bit index
    matches in both bitstrings.
    """

    def __init__(
        self,
        mult_depth: int = 2,
        scale_mod_size: int = 50,
        batch_size: int = 1,
        *,
        challenge_bit: int | None = None,
        bit_length: int = 64,
    ) -> None:
        params = CCParamsCKKSRNS()
        params.SetMultiplicativeDepth(mult_depth)
        params.SetScalingModSize(scale_mod_size)
        params.SetBatchSize(batch_size)

        self.cc: CryptoContext = GenCryptoContext(params)
        self.cc.Enable(PKESchemeFeature.PKE)
        self.cc.Enable(PKESchemeFeature.KEYSWITCH)
        self.cc.Enable(PKESchemeFeature.LEVELEDSHE)

        self.keys = self.cc.KeyGen()
        self.cc.EvalMultKeyGen(self.keys.secretKey)

        self.challenge_bit = (
            secrets.randbits(1) if challenge_bit is None else (challenge_bit & 1)
        )
        if DEBUG_GAME:
            print(f"[DEBUG] challenge_bit = {self.challenge_bit}")
        self.state: List[OracleRow] = []
        self.scale_bits = scale_mod_size
        self.bit_length = bit_length

    # ------------------------------------------------------------------ #
    # Helper utilities

    def _encode(self, value: float) -> Plaintext:
        return self.cc.MakeCKKSPackedPlaintext([value])

    def _to_bits(self, value: float) -> Tuple[int, ...]:
        return float_to_bits(value, self.bit_length, self.scale_bits)

    # ------------------------------------------------------------------ #
    # Oracles

    def enc_oracle(self, m0: float, m1: float) -> Ciphertext:
        pt0 = self._encode(m0)
        pt1 = self._encode(m1)

        chosen_pt = pt0 if self.challenge_bit == 0 else pt1
        ciphertext = self.cc.Encrypt(self.keys.publicKey, chosen_pt)

        row = OracleRow(m0=m0, m1=m1, ciphertext=ciphertext)
        self.state.append(row)
        if DEBUG_GAME:
            self._debug_log_bits(len(self.state) - 1, m0, m1)
        return ciphertext

    def eval_oracle(
        self, indices: Tuple[int, ...], circuit: HomomorphicCKKSFunction
    ) -> Ciphertext:
        if len(indices) != circuit.num_inputs:
            raise ValueError("indices count does not match circuit arity")

        rows: List[OracleRow] = []
        for index in indices:
            if index < 0 or index >= len(self.state):
                raise IndexError("state index out of range")
            rows.append(self.state[index])

        m0_inputs = tuple(row.m0 for row in rows)
        m1_inputs = tuple(row.m1 for row in rows)
        ct_inputs = tuple(row.ciphertext for row in rows)

        new_m0 = circuit.plaintext(m0_inputs)
        new_m1 = circuit.plaintext(m1_inputs)
        new_ct = circuit.ciphertext(self.cc, ct_inputs)

        new_row = OracleRow(m0=new_m0, m1=new_m1, ciphertext=new_ct)
        self.state.append(new_row)
        if DEBUG_GAME:
            self._debug_log_bits(len(self.state) - 1, new_m0, new_m1)
        return new_ct

    def dec_oracle(self, index: int, bit_index: int) -> int | None:
        """
        Decryption oracle: reveals only the selected bit of Dec(Enc(m_b)).
        """
        if index < 0 or index >= len(self.state):
            raise IndexError("state index out of range")
        if bit_index < 0 or bit_index >= self.bit_length:
            raise IndexError("bit index out of range")

        row = self.state[index]
        bits0 = self._to_bits(row.m0)
        bits1 = self._to_bits(row.m1)
        if bits0[bit_index] != bits1[bit_index]:
            return None

        plaintext = self.cc.Decrypt(row.ciphertext, self.keys.secretKey)
        plaintext.SetLength(1)
        value = plaintext.GetRealPackedValue()[0]
        bits = float_to_bits(value, self.bit_length, self.scale_bits)
        bits_str = "".join(str(bit) for bit in bits)
        # print(f"[DEBUG] dec_oracle[{index}] value={value} bits={bits_str}")
        return bits[bit_index]

    # ------------------------------------------------------------------ #
    # Debug helpers

    def _debug_log_bits(self, index: int, m0: float, m1: float) -> None:
        bits0 = "".join(str(bit) for bit in self._to_bits(m0))
        bits1 = "".join(str(bit) for bit in self._to_bits(m1))
        print(f"[DEBUG] state[{index}] m0={m0} bits={bits0}")
        print(f"[DEBUG] state[{index}] m1={m1} bits={bits1}")


class SquareCircuit(HomomorphicCKKSFunction):
    num_inputs = 1

    def plaintext(self, values: Tuple[float, ...]) -> float:
        value = values[0]
        return value * value

    def ciphertext(
        self, cc: CryptoContext, ciphertexts: Tuple[Ciphertext, ...]
    ) -> Ciphertext:
        ciphertext = ciphertexts[0]
        return cc.EvalMult(ciphertext, ciphertext)


class AddCircuit(HomomorphicCKKSFunction):
    num_inputs = 2

    def plaintext(self, values: Tuple[float, ...]) -> float:
        return values[0] + values[1]

    def ciphertext(
        self, cc: CryptoContext, ciphertexts: Tuple[Ciphertext, ...]
    ) -> Ciphertext:
        return cc.EvalAdd(ciphertexts[0], ciphertexts[1])


class MultiplyCircuit(HomomorphicCKKSFunction):
    num_inputs = 2

    def plaintext(self, values: Tuple[float, ...]) -> float:
        return values[0] * values[1]

    def ciphertext(
        self, cc: CryptoContext, ciphertexts: Tuple[Ciphertext, ...]
    ) -> Ciphertext:
        return cc.EvalMult(ciphertexts[0], ciphertexts[1])


def _format_plaintext(plaintext: Plaintext, precision: int = 6) -> str:
    return plaintext.GetFormattedValues(precision)


if __name__ == "__main__":
    game = BitwiseCKKSIndCpaDGame(mult_depth=2, scale_mod_size=50, batch_size=1)

    ct0 = game.enc_oracle(0.125, 1.75)
    print(f"state[0] ciphertext: {ct0}")

    ct1 = game.enc_oracle(-0.5, -0.5)
    print(f"state[1] ciphertext: {ct1}")

    square = SquareCircuit()
    ct_square = game.eval_oracle((0,), square)

    add = AddCircuit()
    ct_add = game.eval_oracle((0, 1), add)

    bit_idx = 10
    bit_value = game.dec_oracle(1, bit_idx)
    if bit_value is None:
        print(f"bit {bit_idx} differs, decryption denied.")
    else:
        print(f"bit {bit_idx} matches, decrypted bit: {bit_value}")
