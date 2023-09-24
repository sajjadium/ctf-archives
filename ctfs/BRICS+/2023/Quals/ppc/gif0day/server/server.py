import asyncio
import hashlib
import os
import random
import string
import tempfile

import grpclib
from grpclib.server import Server
from grpclib.utils import graceful_exit
from pb import restore_grpc
from pb import restore_pb2

from gifgen import generate_gif
from gifcrop import crop_gif


class RestoreService(restore_grpc.RestoreServiceBase):
    def __init__(self, flag: str, num_rounds=10):
        self.flag = flag
        self.num_rounds = num_rounds

    def rnd_uniq_string(self, length: int):
        alpha = list(string.ascii_letters + string.digits)
        random.shuffle(alpha)
        return ''.join(alpha[:length])

    def gen_round(self, rnd: int):
        content = self.rnd_uniq_string(8)
        if rnd == self.num_rounds:
            content = self.flag
        salt = self.rnd_uniq_string(5)
        request = restore_pb2.RestoreRequest(hash=hashlib.md5(f'{content}{salt}'.encode()).hexdigest(), salt=salt)

        with tempfile.NamedTemporaryFile(suffix='.gif') as temp:
            generate_gif(content, temp.name)
            crop_gif(temp.name)
            request.gif = open(temp.name, 'rb').read()
        return request, content

    async def Restore(self, stream: 'grpclib.server.Stream[restore_pb2.Answer, restore_pb2.RestoreRequest]') -> None:
        rnd = 0
        while rnd <= self.num_rounds:
            request, content = self.gen_round(rnd)
            await stream.send_message(request)

            try:
                async with asyncio.timeout(10):
                    answer = await stream.recv_message()
            except asyncio.TimeoutError:
                await stream.send_trailing_metadata(status=grpclib.Status.DEADLINE_EXCEEDED, status_message="Too slow!")
                return
            if answer.answer != content:
                await stream.send_trailing_metadata(status=grpclib.Status.INVALID_ARGUMENT,
                                                    status_message="Wrong answer!")
                return

            rnd += 1

        await stream.send_trailing_metadata()
        return


async def main(*, host='0.0.0.0', port=50051):
    server = grpclib.server.Server([RestoreService(flag=os.getenv('FLAG'), num_rounds=100)])
    with graceful_exit([server]):
        await server.start(host, port)
        print(f'Serving on {host}:{port}', flush=True)
        await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
