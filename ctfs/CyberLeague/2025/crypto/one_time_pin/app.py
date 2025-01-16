#!/usr/bin/env python3

import asyncio
import logging
import random
from pathlib import Path

logger = logging.basicConfig(level=logging.INFO)

HOST = "0.0.0.0"
PORT = 10008
FLAG = Path("flag.txt").read_bytes()


async def print_prompt(writer: asyncio.StreamWriter):
    writer.writelines(
        (
            b"Welcome Admin!\n",
            b"Please enter your 8-char one time pin to continue [00000000 - ffffffff]:",
        )
    )
    await writer.drain()


async def read_pin(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while not (line := await reader.readline()):
        writer.write(b"Please enter a valid PIN\n")
        await writer.drain()
    return int(line.rstrip(), base=16)


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_ip, client_port = reader._transport.get_extra_info("peername")
    logging.info(f"New connection from: {client_ip}:{client_port}")

    rand = random.Random()
    try:
        while True:
            await print_prompt(writer)

            pin = await read_pin(reader, writer)
            num = rand.randrange(2**32 - 1)

            if pin != num:
                delta = abs(pin - num)
                writer.write(f"Error {hex(delta)}: Incorrect PIN.".encode())
            else:
                writer.write(b"Well done! Here is your flag: " + FLAG)
                break

            await writer.drain()
    except Exception as e:
        writer.write(f"Unexpected PIN provided. {e}".encode())
        await writer.drain()
    finally:
        writer.write_eof()
        writer.close()


async def main(host, port):
    srv = await asyncio.start_server(handler, host, port)
    await srv.serve_forever()


if __name__ == "__main__":
    asyncio.run(main(HOST, PORT))
