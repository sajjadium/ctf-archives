from abc import abstractmethod
from secret import flag
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import random
import os
import string
import hashlib


def bxor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])


def expand_key(key, n):
    if len(key) >= n:
        return key[:n]

    out = key + b"\x00" * (n - len(key))
    for i in range(1, n - len(key) + 1):
        out = bxor(out, b"\x00" * i + key + b"\x00" * (n - len(key) - i))
    return out


traffic = []


class AuthClass:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.challenge = None

    def generate_challenge_response(self, challenge_hash):
        password_hash = hashlib.md5(password.encode()).digest()
        challenge_response = DES.new(
            expand_key(password_hash[0:3], 8), DES.MODE_ECB
        ).encrypt(pad(challenge_hash, 16))
        challenge_response += DES.new(
            expand_key(password_hash[7:10], 8), DES.MODE_ECB
        ).encrypt(pad(challenge_hash, 16))
        challenge_response += DES.new(
            expand_key(password_hash[13:16], 8), DES.MODE_ECB
        ).encrypt(pad(challenge_hash, 16))
        return challenge_response

    def generate_auth_response(self, challenge_response, challenge_hash):
        password_hash_hash = hashlib.md5(
            hashlib.md5(self.password.encode()).digest()
        ).digest()
        digest = hashlib.sha1(
            password_hash_hash
            + challenge_response
            + b"Magic server to client signing constant"
        ).digest()
        auth_response = hashlib.sha1(
            digest + challenge_hash + b"Pad to make it do one more iteration"
        ).digest()
        return auth_response

    def generate_challenge(self):
        self.challenge = os.urandom(16)
        return self.challenge

    @abstractmethod
    def send(self, message):
        pass


class Server(AuthClass):
    def __init__(self, username, password):
        super().__init__(username, password)

    def send(self, message):
        traffic.append(("Server", message))


class Client(AuthClass):
    def __init__(self, username, password):
        super().__init__(username, password)

    def generate_client_response(self, server_challenge):
        challenge_hash = hashlib.sha1(
            self.challenge + server_challenge + username.encode()
        ).digest()[:8]
        return (
            self.generate_challenge_response(challenge_hash),
            challenge_hash,
            username,
        )

    def send(self, message):
        traffic.append(("Client", message))


if __name__ == "__main__":
    username = "admin"
    password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(40)
    )

    server = Server(username, password)
    client = Client(username, password)

    client.send("Hello")
    server.generate_challenge()
    server.send(server.challenge)

    client.generate_challenge()
    client_response = client.generate_client_response(server.challenge)
    client.send(client_response)
    challenge_response, challenge_hash, _ = client_response
    assert challenge_response == server.generate_challenge_response(
        challenge_hash
    ), "Error in authenticating client"

    server_auth = server.generate_auth_response(challenge_response, challenge_hash)
    server.send(server_auth)
    assert server_auth == client.generate_auth_response(
        challenge_response, challenge_hash
    ), "Error in authenticating server"

    print("Traffic")
    print(traffic)
    print("Now, your turn!")

    server.generate_challenge()
    print("Server challenge:", server.challenge)

    challenge_response, new_challenge_hash, _username = input(
        "Client response: "
    ).split(" ")
    challenge_response = bytes.fromhex(challenge_response)
    new_challenge_hash = bytes.fromhex(new_challenge_hash)
    assert _username == username
    assert challenge_hash != new_challenge_hash, "No cheating!"
    assert challenge_response == server.generate_challenge_response(
        new_challenge_hash
    ), "Error in authenticating client"

    print("Successfully authenticated!")
    print("Here's your flag", flag)
