import os
import asyncio
from reader.server import handle_client


async def run_server():
    os.chdir("./files/")
    server = await asyncio.start_server(handle_client, "0.0.0.0", 3000)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())
