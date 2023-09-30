from merkle_tree import *
import json
import hashlib
import secrets
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    load_pem_public_key,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flag import flag


class Server:
    merkle_tree: MerkleTree
    usernames: set

    def __init__(self):
        self.merkle_tree = MerkleTree()
        self.usernames = set()

    def register(self, username: str, public_key: bytes):
        if len(username) == 0:
            raise ValueError("Empty username")

        if username in self.usernames:
            raise ValueError("Username is taken")

        key = username.encode()
        value = public_key
        index = hashlib.sha256(key).digest()
        self.merkle_tree.set(index, key, value)
        self.usernames.add(username)

    def query(self, username: str) -> AuthenticationPath:
        key = username.encode()
        index = hashlib.sha256(key).digest()
        return self.merkle_tree.get(index)


def generate_random_users(server):
    for i in range(256):
        username = f"user_{random.randbytes(4).hex()}"
        private_key = ec.generate_private_key(ec.SECP256R1())
        server.register(
            username,
            private_key.public_key().public_bytes(
                Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
            ),
        )


def bob_query_self(server, bob_public_key):
    print()
    print("Bob is querying his own key...")
    bob_ap = server.query("bob")
    if bob_ap.proof_type() != AuthenticationPath.proof_of_inclusion:
        raise ValueError("Bob expected a proof of inclusion")
    result, error = bob_ap.verify(bob_public_key, server.merkle_tree.root_hash)
    if not result:
        raise ValueError(f"Bob failed to verify authentication path: {error}")

    print("Bob successfully queried his own key!")
    print(f"Bob's authentication path was:\n{json.dumps(bob_ap.json_dict())}")
    return bob_ap


def prompt_for_registration(server):
    print("Please register your username and public key with the server!")
    username = input("Enter your username: ")
    if type(username) is not str and len(username) == 0:
        raise ValueError("Invalid username")
    public_key = bytes.fromhex(input("Enter your public key in hex: "))
    server.register(username, public_key)
    ap = server.query(username)
    print("Successfully registered!")


def main():
    server = Server()
    generate_random_users(server)

    alice_private_key = ec.generate_private_key(ec.SECP256R1())
    alice_public_key = alice_private_key.public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    )
    server.register("alice", alice_public_key)
    print(f"Alice's public key is {alice_public_key.hex()}")

    bob_private_key = ec.generate_private_key(ec.SECP256R1())
    bob_public_key = bob_private_key.public_key().public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    )
    server.register("bob", bob_public_key)
    print(f"Bob's public key is {alice_public_key.hex()}")

    bob_ap = bob_query_self(server, bob_public_key)

    prompt_for_registration(server)

    print()
    print("Alice is querying for Bob's public key.")
    print("But YOU are able to intercept this query and modify the username!")
    s = input("Please specify a username: ")
    if "bob" not in s:
        raise ValueError("Username is too suspicious")
    ap = server.query(s)

    result, error = ap.verify(None, server.merkle_tree.root_hash)
    if not result:
        raise ValueError(f"Alice failed peer validation of Bob: {error}")
    if ap.proof_type() != AuthenticationPath.proof_of_inclusion:
        raise ValueError("Alice expected a proof of inclusion")
    if (
        bytes_to_bits(bob_ap.lookup_index)[: bob_ap.leaf.level]
        != bytes_to_bits(ap.lookup_index)[: bob_ap.leaf.level]
    ):
        raise ValueError("This authentication path isn't for Bob")

    print("Alice successfully verified the authentication path to Bob's public key!")
    print("Alice is sending the flag to Bob encrypted with his public key:")

    shared_key = alice_private_key.exchange(ec.ECDH(), load_pem_public_key(ap.leaf.value))  # type: ignore
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=None,
    ).derive(shared_key)

    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(flag) + encryptor.finalize()
    print(f"Ciphertext: {ct.hex()}")
    print(f"IV: {iv.hex()}")


if __name__ == "__main__":
    main()
