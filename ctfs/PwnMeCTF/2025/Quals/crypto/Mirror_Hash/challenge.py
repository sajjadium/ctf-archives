import hashlib
import struct
from secret import FLAG

class CustomSHA:
    def __init__(self, data: bytes):
        self.data: bytes = data

    def process(self) -> str:
        h0 = 0x674523EFCD.to_bytes(5, byteorder='big')
        h = h0
        data = self.preprocess()

        for i in range(0, len(data), 8):
            chunk = data[i:i+8]

            h = hashlib.sha256(chunk + h).digest()[:5]

        return f'{h.hex()}'

    def preprocess(self) -> bytes:
        data = self.data
        data = bytearray(data)

        data.append(0x80)
        while len(data) % 8 != 0:
            data.append(0x00)

        data += struct.pack('>Q', 8 * len(self.data))

        return bytes(data)


    def sha_custom(self):
        return self.process()

with open("Hack.zip", "rb") as f:
    data_hack = f.read()
    CustomSHA(data_hack)
    sha_custom_hack = CustomSHA(data_hack).sha_custom()


def challenge(received_json):
    response_json = {}
    if 'action' in received_json:
        if received_json['action'] == 'hash':
            if 'data' in received_json:
                data = bytes.fromhex(received_json['data'])
                if data == data_hack:
                    response_json['error'] = "Forbidden data"
                else:
                    sha_custom = CustomSHA(data)
                    response_json['hash'] = sha_custom.sha_custom()

                    if sha_custom_hack == response_json['hash']:
                        response_json['flag'] = FLAG
            else:
                response_json['error'] = 'No data provided'
        else:
            response_json['error'] = 'Invalid action'
    else:
        response_json['error'] = 'No action provided'

    return response_json
