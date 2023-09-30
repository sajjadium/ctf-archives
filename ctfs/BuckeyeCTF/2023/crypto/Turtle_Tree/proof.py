from util import *
import hashlib
import struct


class ProofNode:
    level: int
    index: bytes
    value: bytes | None

    def hash(self, tree_nonce: bytes) -> bytes:
        h = b""
        if self.value == None:
            h = hashlib.sha256(
                empty_node_identifier
                + tree_nonce
                + self.index
                + struct.pack("<I", self.level)
            ).digest()
        else:
            h = hashlib.sha256(
                leaf_node_identifier
                + tree_nonce
                + self.index
                + struct.pack("<I", self.level)
                + self.value
            ).digest()
        return h

    def json_dict(self) -> dict:
        return {
            "level": self.level,
            "index": self.index.hex(),
            "value": self.value.hex() if self.value != None else None,
        }


class AuthenticationPath:
    tree_nonce: bytes
    pruned_tree: list[bytes]
    lookup_index: bytes
    leaf: ProofNode

    proof_of_inclusion = 0
    proof_of_absence = 1

    def __init__(self):
        self.pruned_tree = []

    def auth_path_hash(self) -> bytes:
        h = self.leaf.hash(self.tree_nonce)
        index_bits = bytes_to_bits(self.leaf.index)
        depth = self.leaf.level
        while depth > 0:
            depth -= 1
            if index_bits[depth]:
                h = hashlib.sha256(self.pruned_tree[depth] + h).digest()
            else:
                h = hashlib.sha256(h + self.pruned_tree[depth]).digest()
        return h

    def proof_type(self):
        if self.lookup_index == self.leaf.index:
            return AuthenticationPath.proof_of_inclusion
        else:
            return AuthenticationPath.proof_of_absence

    def verify(self, value: bytes | None, tree_hash: bytes) -> tuple[bool, str | None]:
        if self.proof_type() == AuthenticationPath.proof_of_absence:
            index_bits = bytes_to_bits(self.leaf.index)
            lookup_index_bits = bytes_to_bits(self.lookup_index)
            if index_bits[: self.leaf.level] != lookup_index_bits[: self.leaf.level]:
                return (
                    False,
                    "Lookup index is inconsistent with index of the proof node",
                )
        else:
            if value != None and value != self.leaf.value:
                return (False, "Value does not match")

        if tree_hash != self.auth_path_hash():
            return (False, "Authentication path hash does not match provided tree hash")

        return (True, None)

    def json_dict(self) -> dict:
        return {
            "tree_nonce": self.tree_nonce.hex(),
            "pruned_tree": [x.hex() for x in self.pruned_tree],
            "lookup_index": self.lookup_index.hex(),
            "leaf": self.leaf.json_dict(),
        }
