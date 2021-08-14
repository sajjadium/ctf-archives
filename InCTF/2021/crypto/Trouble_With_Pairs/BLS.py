from typing import (
    Sequence,
)
from math import (
    ceil,
    log2,
)
import abc
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    ValidationError,
)
from hashlib import sha256

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
    G2,
)

from py_ecc.bls.hash import (
    hkdf_expand,
    hkdf_extract,
    i2osp,
    os2ip,
)
# from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.bls.g2_primitives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
    subgroup_check,
    is_inf,
)


def hash_to_G2(msg, DST, hash):
    m = int(hash(msg).hexdigest(),16)
    return  multiply(G2,m)


class BaseG2Ciphersuite(abc.ABC):
    DST = b''
    xmd_hash_function = sha256

    #
    # Input validation helpers
    #
    @staticmethod
    def _is_valid_privkey(privkey: int) -> bool:
        return isinstance(privkey, int) and privkey > 0 and privkey < curve_order

    @staticmethod
    def _is_valid_pubkey(pubkey: bytes) -> bool:
        # SV: minimal-pubkey-size
        return isinstance(pubkey, bytes) and len(pubkey) == 48

    @staticmethod
    def _is_valid_message(message: bytes) -> bool:
        return isinstance(message, bytes)

    @staticmethod
    def _is_valid_signature(signature: bytes) -> bool:
        # SV: minimal-pubkey-size
        return isinstance(signature, bytes) and len(signature) == 96

    #
    # APIs
    #
    @classmethod
    def SkToPk(cls, privkey: int) -> BLSPubkey:
        """
        The SkToPk algorithm takes a secret key SK and outputs the
        corresponding public key PK.
        Raise `ValidationError` when there is input validation error.
        """
        try:
            # Inputs validation
            assert cls._is_valid_privkey(privkey)
        except Exception as e:
            raise ValidationError(e)

        # Procedure
        return G1_to_pubkey(multiply(G1, privkey))

    @classmethod
    def KeyGen(cls, IKM: bytes, key_info: bytes = b'') -> int:
        salt = b'BLS-SIG-KEYGEN-SALT-'
        SK = 0
        while SK == 0:
            salt = cls.xmd_hash_function(salt).digest()
            prk = hkdf_extract(salt, IKM + b'\x00')
            l = ceil((1.5 * ceil(log2(curve_order))) / 8)  # noqa: E741
            okm = hkdf_expand(prk, key_info + i2osp(l, 2), l)
            SK = os2ip(okm) % curve_order
        return SK

    @staticmethod
    def KeyValidate(PK: BLSPubkey) -> bool:
        try:
            pubkey_point = pubkey_to_G1(PK)
        except (ValidationError, ValueError, AssertionError):
            return False

        if is_inf(pubkey_point):
            return False

        if not subgroup_check(pubkey_point):
            return False

        return True

    @classmethod
    def _CoreSign(cls, SK: int, message: bytes, DST: bytes) -> BLSSignature:
        """
        The CoreSign algorithm computes a signature from SK, a secret key,
        and message, an octet string.
        Raise `ValidationError` when there is input validation error.
        """
        try:
            # Inputs validation
            assert cls._is_valid_privkey(SK)
            assert cls._is_valid_message(message)
        except Exception as e:
            raise ValidationError(e)

        # Procedure
        message_point = hash_to_G2(message, DST, cls.xmd_hash_function)
        signature_point = multiply(message_point, SK)
        return G2_to_signature(signature_point)

    @classmethod
    def _CoreVerify(cls, PK: BLSPubkey, message: bytes,
                    signature: BLSSignature, DST: bytes) -> bool:
        try:
            # Inputs validation
            assert cls._is_valid_pubkey(PK)
            assert cls._is_valid_message(message)
            assert cls._is_valid_signature(signature)

            # Procedure
            assert cls.KeyValidate(PK)
            signature_point = signature_to_G2(signature)
            if not subgroup_check(signature_point):
                return False
            final_exponentiation = final_exponentiate(
                pairing(
                    signature_point,
                    G1,
                    final_exponentiate=False,
                ) * pairing(
                    hash_to_G2(message, DST, cls.xmd_hash_function),
                    neg(pubkey_to_G1(PK)),
                    final_exponentiate=False,
                )
            )
            return final_exponentiation == FQ12.one()
        except (ValidationError, ValueError, AssertionError):
            return False

    @classmethod
    def Aggregate(cls, signatures: Sequence[BLSSignature]) -> BLSSignature:
        """
        The Aggregate algorithm aggregates multiple signatures into one.
        Raise `ValidationError` when there is input validation error.
        """
        try:
            # Inputs validation
            for signature in signatures:
                assert cls._is_valid_signature(signature)

            # Preconditions
            assert len(signatures) >= 1
        except Exception as e:
            raise ValidationError(e)

        # Procedure
        aggregate = Z2  # Seed with the point at infinity
        for signature in signatures:
            signature_point = signature_to_G2(signature)
            aggregate = add(aggregate, signature_point)
        return G2_to_signature(aggregate)

    @classmethod
    def _CoreAggregateVerify(cls, PKs: Sequence[BLSPubkey], messages: Sequence[bytes],
                             signature: BLSSignature, DST: bytes) -> bool:
        try:
            # Inputs validation
            for pk in PKs:
                assert cls._is_valid_pubkey(pk)
            for message in messages:
                assert cls._is_valid_message(message)
            assert len(PKs) == len(messages)
            assert cls._is_valid_signature(signature)

            # Preconditions
            assert len(PKs) >= 1

            # Procedure
            signature_point = signature_to_G2(signature)
            if not subgroup_check(signature_point):
                return False
            aggregate = FQ12.one()
            for pk, message in zip(PKs, messages):
                assert cls.KeyValidate(pk)
                pubkey_point = pubkey_to_G1(pk)
                message_point = hash_to_G2(message, DST, cls.xmd_hash_function)
                aggregate *= pairing(message_point,
                                     pubkey_point, final_exponentiate=False)
            aggregate *= pairing(signature_point, neg(G1),
                                 final_exponentiate=False)
            return final_exponentiate(aggregate) == FQ12.one()

        except (ValidationError, ValueError, AssertionError):
            return False

    @classmethod
    def Sign(cls, SK: int, message: bytes) -> BLSSignature:
        return cls._CoreSign(SK, message, cls.DST)

    @classmethod
    def Verify(cls, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return cls._CoreVerify(PK, message, signature, cls.DST)

    @abc.abstractclassmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        ...


class G2Basic(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_'

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        if len(messages) != len(set(messages)):  # Messages are not unique
            return False
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)


class G2MessageAugmentation(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_AUG_'

    @classmethod
    def Sign(cls, SK: int, message: bytes) -> BLSSignature:
        PK = cls.SkToPk(SK)
        return cls._CoreSign(SK, PK + message, cls.DST)

    @classmethod
    def Verify(cls, PK: BLSPubkey, message: bytes, signature: BLSSignature) -> bool:
        return cls._CoreVerify(PK, PK + message, signature, cls.DST)

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        if len(PKs) != len(messages):
            return False
        messages = [pk + msg for pk, msg in zip(PKs, messages)]
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)


class G2ProofOfPossession(BaseG2Ciphersuite):
    DST = b'BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_'
    POP_TAG = b'BLS_POP_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_'

    @classmethod
    def _is_valid_pubkey(cls, pubkey: bytes) -> bool:
        """
        Note: PopVerify is a precondition for -Verify APIs
        However, it's difficult to verify it with the API interface in runtime.
        To ensure KeyValidate has been checked, we check it in the input validation.
        See https://github.com/cfrg/draft-irtf-cfrg-bls-signature/issues/27 for the discussion.
        """
        if not super()._is_valid_pubkey(pubkey):
            return False
        return cls.KeyValidate(BLSPubkey(pubkey))

    @classmethod
    def AggregateVerify(cls, PKs: Sequence[BLSPubkey],
                        messages: Sequence[bytes], signature: BLSSignature) -> bool:
        return cls._CoreAggregateVerify(PKs, messages, signature, cls.DST)

    @classmethod
    def PopProve(cls, SK: int) -> BLSSignature:
        pubkey = cls.SkToPk(SK)
        return cls._CoreSign(SK, pubkey, cls.POP_TAG)

    @classmethod
    def PopVerify(cls, PK: BLSPubkey, proof: BLSSignature) -> bool:
        return cls._CoreVerify(PK, PK, proof, cls.POP_TAG)

    @staticmethod
    def _AggregatePKs(PKs: Sequence[BLSPubkey]) -> BLSPubkey:
        """
        Aggregate the public keys.
        Raise `ValidationError` when there is input validation error.
        """
        try:
            assert len(PKs) >= 1, 'Insufficient number of PKs. (n < 1)'
        except Exception as e:
            raise ValidationError(e)

        aggregate = Z1  # Seed with the point at infinity
        for pk in PKs:
            pubkey_point = pubkey_to_G1(pk)
            aggregate = add(aggregate, pubkey_point)
        return G1_to_pubkey(aggregate)

    @classmethod
    def FastAggregateVerify(cls, PKs: Sequence[BLSPubkey],
                            message: bytes, signature: BLSSignature) -> bool:
        try:
            # Inputs validation
            for pk in PKs:
                assert cls._is_valid_pubkey(pk)
            assert cls._is_valid_message(message)
            assert cls._is_valid_signature(signature)

            # Preconditions
            assert len(PKs) >= 1

            # Procedure
            aggregate_pubkey = cls._AggregatePKs(PKs)
        except (ValidationError, AssertionError):
            return False
        else:
            return cls.Verify(aggregate_pubkey, message, signature)
