import asyncio
import concurrent.futures
import traceback
from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from nth_root import nth_root, chinese_remainder # not provided

class Server:
    def __init__(self):
        e = 17
        nbits = 512

        p = getPrime(nbits)
        q = getPrime(nbits)
        N = p * q

        self.p = p
        self.q = q
        self.N = N
        self.e = e

    def encrypt(self, m):
        assert 0 <= m < self.N
        c = pow(m, self.e, self.N)
        return int(c)

    def decrypt(self, c):
        assert 0 <= c < self.N
        mp = int(nth_root(c, self.p, self.e))
        mq = int(nth_root(c, self.q, self.e))
        m = chinese_remainder([mp, mq], [self.p, self.q])
        return int(m)

    def encrypt_flag(self):
        with open("flag.txt", "rb") as f:
            flag = f.read()

        key = RSA.construct((self.N, self.e))
        cipher = PKCS1_OAEP.new(key)
        c = cipher.encrypt(flag)
        c = bytes_to_long(c)
        return c


async def handle(a):
    S = await a.run(Server)
    while True:
        cmd = (await a.input("Enter your option (EDF) > ")).strip()
        if cmd == "E":
            m = int(await a.input("Enter your integer to encrypt > "))
            c = await a.run(S.encrypt, m)
            await a.print(str(c) + '\n')
        elif cmd == "D":
            c = int(await a.input("Enter your integer to decrypt > "))
            m = await a.run(S.decrypt, c)
            await a.print(str(m) + '\n')
        elif cmd == "F":
            c = await a.run(S.encrypt_flag)
            await a.print(str(c) + '\n')
            return

class Handler:
    def __init__(self, reader, writer, pool):
        self.reader = reader
        self.writer = writer
        self.pool = pool
    async def print(self, data):
        self.writer.write(str(data).encode())
        await self.writer.drain()
    async def input(self, prompt):
        await self.print(prompt)
        return (await self.reader.readline()).decode()
    async def run(self, func, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.pool, func, *args)
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_t, exc_v, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()
        if exc_v is not None and not isinstance(exc_v, asyncio.TimeoutError):
            traceback.print_exception(exc_v)
        return True


async def main():
    with concurrent.futures.ProcessPoolExecutor() as pool:
        async def callback(reader, writer):
            async with Handler(reader, writer, pool) as a:
                await asyncio.wait_for(handle(a), 20)
        server = await asyncio.start_server(callback, '0.0.0.0', 5000)
        print('listening')
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
