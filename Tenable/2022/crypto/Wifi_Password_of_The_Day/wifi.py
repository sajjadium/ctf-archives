import zlib
import json
from Crypto.Cipher import AES
import logging
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import base64

# wifi password
current_wifi_password = "flag{test_123}"

# 128 bit key
encryption_key = b'testing123456789'

def encrypt_wifi_data(user):
    global current_wifi_password, encryption_key

    wifi_data = {"user:": user,
                 "pass:": current_wifi_password}

    to_send = json.dumps(wifi_data)

    msg = zlib.compress(to_send.encode('utf-8'))

    text_padded = msg + (AES.block_size - (len(msg) % AES.block_size)) * b'\x00'

    logging.info("sending wifi password to user %s" + user)

    iv = 16 * b'\x00'
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)

    cipher_enc = cipher.encrypt(text_padded)
    return cipher_enc


class Challenge(Protocol):

    def dataReceived(self, data):
        username = data.strip()
        data = encrypt_wifi_data(username.decode('utf-8'))
        self.transport.write(base64.b64encode(data) + b'\r\n')
        self.transport.write(b"Enter username: ")

    def connectionMade(self):
        self.transport.write(b"Welcome to Wifi Password of the Day Server\r\n")
        self.transport.write(b"Enter username: ")

    def __init__(self, factory):
        self.factory = factory
        self.debug = True

class ChallengeFactory(Factory):
    protocol = Challenge

    def buildProtocol(self, addr):
        return Challenge(self)

reactor.listenTCP(1234, ChallengeFactory())
reactor.run()
