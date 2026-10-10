#!/usr/bin/env python3
"""
one-more client.  The service speaks one command per WebSocket message.

    python3 client.py wss://HOST
        Interactive. Type commands, or pipe a script in:
            printf 'open\nopen\nquit\n' | python3 client.py wss://HOST

    python3 client.py wss://HOST --listen 1337
        Bridge. Exposes the service as a plain TCP port on 127.0.0.1, so you
        can drive it the usual way:
            nc 127.0.0.1 1337
        Every TCP connection gets its own independent service instance.

Needs:  pip install websockets
"""
import asyncio
import sys

LINE_LIMIT = 16 << 20     # a submit line is ~70 KB

from websockets.asyncio.client import connect


async def pump_interactive(url):
    async with connect(url, max_size=None, ping_interval=20) as ws:
        loop = asyncio.get_running_loop()

        async def reader():
            try:
                async for msg in ws:
                    print(msg, flush=True)
            except Exception:
                pass

        task = asyncio.create_task(reader())
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            await ws.send(line.rstrip("\n"))
            if line.split()[:1] == ["quit"]:
                break
        await asyncio.sleep(0.5)      # let trailing replies land
        task.cancel()


async def bridge(url, port):
    async def on_tcp(tcp_r, tcp_w):
        try:
            async with connect(url, max_size=None, ping_interval=20) as ws:
                async def ws_to_tcp():
                    async for msg in ws:
                        tcp_w.write((msg + "\n").encode())
                        await tcp_w.drain()

                async def tcp_to_ws():
                    while True:
                        line = await tcp_r.readline()
                        if not line:
                            return
                        await ws.send(line.decode("utf-8", "replace").rstrip("\n"))

                done, pending = await asyncio.wait(
                    [asyncio.create_task(ws_to_tcp()),
                     asyncio.create_task(tcp_to_ws())],
                    return_when=asyncio.FIRST_COMPLETED)
                for t in pending:
                    t.cancel()
                for t in done:        # never let a task failure close us silently
                    exc = t.exception()
                    if exc is not None:
                        raise exc
        except Exception as e:
            try:
                tcp_w.write(f"err bridge: {e}\n".encode())
                await tcp_w.drain()
            except Exception:
                pass
        finally:
            try:
                tcp_w.close()
            except Exception:
                pass

    # submit carries ~70 KB on one line; the default 64 KiB limit truncates it
    srv = await asyncio.start_server(on_tcp, "127.0.0.1", port, limit=LINE_LIMIT)
    print(f"bridging {url}  ->  nc 127.0.0.1 {port}", file=sys.stderr)
    async with srv:
        await srv.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip())
    url = sys.argv[1]
    if "--listen" in sys.argv:
        port = int(sys.argv[sys.argv.index("--listen") + 1])
        asyncio.run(bridge(url, port))
    else:
        asyncio.run(pump_interactive(url))
