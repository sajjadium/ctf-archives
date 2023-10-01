from secret import flag
import hashlib
import random
import os
import ast

DIGEST_SIZE = 256
HEIGHT = 6

def hash(m):
    return hashlib.sha256(m).digest()


class Node:
    def __init__(self, left, right, parent=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hash(self.left.hash + self.right.hash)

    def __repr__(self):
        return self.hash.hex()


class Leaf(Node):
    def __init__(self, value, parent=None):
        self.hash = hash(value)
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        return self.hash.hex()

class MerkleTree:
    def __init__(self, values):
        self.leaves = [Leaf(value) for value in values]
        self.root = self.build_tree(self.leaves)
        self.pubkey = self.root.hash

    def build_tree(self, leaves):
        if len(leaves) == 1:
            return leaves[0]

        parents = []

        for i in range(0, len(leaves), 2):
            left = leaves[i]
            if i + 1 < len(leaves):
                right = leaves[i + 1]
            else:
                right = left

            parent = Node(left, right)
            left.parent = parent
            right.parent = parent
            parents.append(parent)

        return self.build_tree(parents)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node is not None:
            if node.left is not None or node.right is not None:
                self.print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.hash.hex())
            if node.left is not None:
                self.print_tree(node.left, level + 1)


class MerkleSignature:
    def __init__(self, h):
        self.h = h
        self.keypairs = [MerkleSignature._generate_keypair() for _ in range(2 ** self.h)]
        self.tree = MerkleTree([MerkleSignature._serialize_pubkey(keypair[0]) for keypair in self.keypairs])

    @staticmethod
    def _serialize_pubkey(key):
        # reduce the 2-dimensional pubkey into a bytearray for hashing
        return b''.join(key[0] + key[1])

    @staticmethod
    def _generate_keypair():
        priv = [[os.urandom(32) for j in range(DIGEST_SIZE)] for i in range(2)]
        pub = [[hash(priv[i][j]) for j in range(DIGEST_SIZE)] for i in range(2)]
        return pub, priv

    @staticmethod
    def _sign_ots(msg, priv):
        msg_bin = bin(int.from_bytes(hash(msg), 'big'))[2:].zfill(DIGEST_SIZE)
        return [priv[m == "1"][i] for i, m in enumerate(msg_bin)]

    @staticmethod
    def _verify_ots(msg, sig, pub):
        msg_bin = bin(int.from_bytes(hash(msg), 'big'))[2:].zfill(DIGEST_SIZE)
        return all(hash(priv) == pub[m == "1"][i] for i, (m, priv) in enumerate(zip(msg_bin, sig)))


    def sign(self, msg):
        idx = random.randint(0, 2 ** self.h - 1)
        pub, priv = self.keypairs[idx]
        current = self.tree.leaves[idx]
        signature_path = []

        msg_sig = MerkleSignature._sign_ots(msg, priv)

        while current != self.tree.root:
            if current == current.parent.left:
                signature_path.append((current.parent.right.hash, True))
            else:
                signature_path.append((current.parent.left.hash, False))

            current = current.parent

        return (signature_path, msg_sig, pub)


    def verify(self, msg, signature):
        signature_path, sig, pub = signature
        assert MerkleSignature._verify_ots(msg, sig, pub), f"Invalid signature for {msg}!"

        current_hash = hash(MerkleSignature._serialize_pubkey(pub))
        for h, left in signature_path:
            if left:
                current_hash = hash(current_hash + h)
            else:
                current_hash = hash(h + current_hash)

        return current_hash == self.tree.root.hash

if __name__ == "__main__":
    s = MerkleSignature(HEIGHT)
    print("""Welcome! To win, please submit a valid signature containing "flag".
1. Sign a message
2. Verify a message
3. Get root hash""")
    for _ in range(500):
        option = int(input("> "))
        if option == 1:
            msg = input("> ").encode()
            if b'flag' in msg:
                print("No cheating!")
                exit()

            signature_path, msg_sig, pub = s.sign(msg)
            assert s.verify(msg, (signature_path, msg_sig, pub))

            hint = random.sample([node[0].hex() for node in signature_path], HEIGHT // 2)
            random.shuffle(hint)
            print(",".join(hint))
            print(",".join([k.hex() for k in msg_sig]))
        elif option == 2:
            msg = input("> ").encode()
            signature_path = ast.literal_eval(input("> "))
            msg_sig = ast.literal_eval(input("> "))
            pub = ast.literal_eval(input("> "))

            '''
            signature_path: [(bytes, True), (bytes, False), ...]
            msg_sig: [bytes, bytes, bytes, ]
            pub (2, 256) = [[bytes, bytes, ...], [bytes, bytes]]            
            '''
            assert isinstance(signature_path, list) and all([isinstance(node[0], bytes) and isinstance(node[1], bool) for node in signature_path])
            assert isinstance(msg_sig, list) and all(isinstance(i, bytes) for i in msg_sig)
            assert isinstance(pub, list) and all(isinstance(i, list) for i in pub) and all(isinstance(j, bytes) for i in pub for j in i)
            assert s.verify(msg, (signature_path, msg_sig, pub)), "Invalid signature!"

            # Check lengths
            assert len(signature_path) == HEIGHT
            assert len(pub) == 2 and len(pub[0]) == 256 and len(pub[1]) == 256
            assert len(msg_sig) == 256

            if b'flag' in msg:
                print("Well done! Here's your flag:", flag)
            else:
                print("Valid signature!")
        elif option == 3:
            print(s.tree.root.hash.hex())
        else:
            print("Invalid option, try again.")
