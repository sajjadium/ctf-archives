Can you break AES and capture the flag?

    nc aes.uctf.ir 7001

Server source code

import logging

import os
import random
import time
import base64

import asyncio
from asyncio import StreamReader, StreamWriter, TimeoutError

from Crypto.Cipher import AES

class CryptorServer:
    MAX_INPUT_LEN = 64
    IV_LEN = 8

    def __init__(self, key: str, flag: str, host: str = '0.0.0.0', port: int = 7000, timeout: float = 8) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

        self.__key = bytes.fromhex(key)
        self.__flag = flag.encode('utf-8')

    async def run(self) -> None:
        server = await asyncio.start_server(self.__client_handler, host=self.host, port=self.port)
        await server.serve_forever()

    def __encrypt(self, message: bytes) -> bytes:
        random.seed(int(time.time()) * len(message))
        nonce = random.randbytes(CryptorServer.IV_LEN)

        cipher = AES.new(self.__key, AES.MODE_CTR, nonce=nonce)
        ciphertext = cipher.encrypt(message)

        return base64.b64encode((nonce + ciphertext)) + b'\n'

    async def __client_handler(self, reader: StreamReader, writer: StreamWriter) -> None:
        peer_ip, peer_port = writer.get_extra_info('peername')
        peer_name = f'[{peer_ip}]:{peer_port}'

        logging.info(f'New session for {peer_name}')
        try:
            writer.write(b'Encrypted flag: ' + self.__encrypt(self.__flag))
            writer.write(b"Give me a message and I'll encrypt it for you: ")
            await writer.drain()

            user_input = (await asyncio.wait_for(reader.readline(), self.timeout)).strip()
            if len(user_input) < CryptorServer.MAX_INPUT_LEN:
                enc = self.__encrypt(user_input.strip())
                writer.write(enc)
                await writer.drain()
        except TimeoutError:
            logging.warning(f'{peer_name} timed-out')
            return
        except ConnectionError:
            logging.warning(f'Connection error occurred for {peer_name}')
            return
        finally:
            logging.info(f'Session finished for {peer_name}')
            writer.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    flag = os.environ['CRYPTOR_FLAG']
    key = os.environ['CRYPTOR_KEY']

    server = CryptorServer(key, flag)
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logging.info('Bye bye!')
