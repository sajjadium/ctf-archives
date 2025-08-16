from Crypto.Util.number import bytes_to_long
from hashlib import shake_128
from ast import literal_eval
from secrets import token_bytes
from math import floor, ceil, log2
import os

FLAG = os.getenv("FLAG", "SEKAI{}")
m = 256
w = 21
n = 128
l1 = ceil(m / log2(w))
l2 = floor(log2(l1*(w-1)) / log2(w)) + 1
l = l1 + l2

class WOTS:
    def __init__(self):
        self.sk = [token_bytes(n // 8) for _ in range(l)]
        self.pk = [WOTS.chain(sk, w - 1) for sk in self.sk]
    
    def sign(self, digest: bytes) -> list[bytes]:
        assert 8 * len(digest) == m
        d1 = WOTS.pack(bytes_to_long(digest), l1, w)
        checksum = sum(w-1-i for i in d1)
        d2 = WOTS.pack(checksum, l2, w)
        d = d1 + d2

        sig = [WOTS.chain(self.sk[i], w - d[i] - 1) for i in range(l)]
        return sig

    def get_pubkey_hash(self) -> bytes:
        hasher = shake_128(b"\x04")
        for i in range(l):
            hasher.update(self.pk[i])
        return hasher.digest(16)

    @staticmethod
    def pack(num: int, length: int, base: int) -> list[int]:
        packed = []
        while num > 0:
            packed.append(num % base)
            num //= base
        if len(packed) < length:
            packed += [0] * (length - len(packed))
        return packed
    
    @staticmethod
    def chain(x: bytes, n: int) -> bytes:
        if n == 0:
            return x
        x = shake_128(b"\x03" + x).digest(16)
        return WOTS.chain(x, n - 1)

    @staticmethod
    def verify(digest: bytes, sig: list[bytes]) -> bytes:
        d1 = WOTS.pack(bytes_to_long(digest), l1, w)
        checksum = sum(w-1-i for i in d1)
        d2 = WOTS.pack(checksum, l2, w)
        d = d1 + d2

        sig_pk = [WOTS.chain(sig[i], d[i]) for i in range(l)]
        hasher = shake_128(b"\x04")
        for i in range(len(sig_pk)):
            hasher.update(sig_pk[i])
        sig_hash = hasher.digest(16)
        return sig_hash

class MerkleTree:
    def __init__(self, height: int = 8):
        self.h = height
        self.keys = [WOTS() for _ in range(2**height)]
        self.tree = []
        self.root = self.build_tree([key.get_pubkey_hash() for key in self.keys])
    
    def build_tree(self, leaves: list[bytes]) -> bytes:
        self.tree.append(leaves)

        if len(leaves) == 1:
            return leaves[0]
        
        parents = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            if i + 1 < len(leaves):
                right = leaves[i + 1]
            else:
                right = leaves[i]
            hasher = shake_128(b"\x02" + left + right).digest(16)
            parents.append(hasher)
        
        return self.build_tree(parents)

    def sign(self, index: int, digest: bytes) -> list:
        assert 0 <= index < len(self.keys)
        key = self.keys[index]
        wots_sig = key.sign(digest)
        sig = [wots_sig]
        for i in range(self.h):
            leaves = self.tree[i]
            u = index >> i
            if u % 2 == 0:
                if u + 1 < len(leaves):
                    sig.append((0, leaves[u + 1]))
                else:
                    sig.append((0, leaves[u]))
            else:
                sig.append((1, leaves[u - 1]))
        return sig
    
    @staticmethod
    def verify(sig: list, digest: bytes) -> bytes:
        wots_sig = sig[0]
        sig = sig[1:]
        pk_hash = WOTS.verify(digest, wots_sig)
        root_hash = pk_hash
        for (side, leaf) in sig:
            if side == 0:
                root_hash = shake_128(b"\x02" + root_hash + leaf).digest(16)
            else:
                root_hash = shake_128(b"\x02" + leaf + root_hash).digest(16)
        return root_hash

class Challenge:
    def __init__(self, h: int = 8):
        self.h = h
        self.max_signs = 2 ** h - 1
        self.tree = MerkleTree(h)
        self.root = self.tree.root
        self.used = set()
        self.before_input = f"public key: {self.root.hex()}"
    
    def sign(self, num_sign: int, inds: list, messages: list):
        assert num_sign + len(self.used) <= self.max_signs
        assert len(inds) == len(set(inds)) == len(messages) == num_sign
        assert self.used.isdisjoint(inds)
        assert all(b"flag" not in msg for msg in messages)
        sigs = []
        for i in range(num_sign):
            digest = shake_128(b"\x00" + messages[i]).digest(32)
            sigs.append(self.tree.sign(inds[i], digest))
        self.used.update(inds)
        return sigs

    def next(self):
        new_tree = MerkleTree(self.h)
        digest = shake_128(b"\x01" + new_tree.root).digest(32)
        index = next(i for i in range(2 ** self.h) if i not in self.used)
        sig = new_tree.sign(index, digest)
        self.tree = new_tree
        return {
            "root": new_tree.root,
            "sig": sig,
            "index": index,
        }

    def verify(self, sig: list, message: bytes):
        digest = shake_128(b"\x00" + message).digest(32)
        for i, s in enumerate(reversed(sig)):
            if i != 0:
                digest = shake_128(b"\x01" + digest).digest(32)
            digest = MerkleTree.verify(s, digest)
        return digest == self.root

    def get_flag(self, sig: list):
        if not self.verify(sig, b"Give me the flag"):
            return {"message": "Invalid signature"}
        else:
            return {"message": f"Congratulations! Here is your flag: {FLAG}"}

    def __call__(self, type: str, **kwargs):
        assert type in ["sign", "next", "get_flag"]
        return getattr(self, type)(**kwargs)

challenge = Challenge()
print(challenge.before_input)
try:
    while True:
        print(challenge(**literal_eval(input("input: "))))
except:
    exit(1)
