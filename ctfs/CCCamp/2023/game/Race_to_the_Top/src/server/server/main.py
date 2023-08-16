import argparse
import logging
import os
import sys
import tempfile
from asyncio import get_event_loop
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from threading import Event
from typing import cast

import dill
from rpyc.core import SlaveService
from rpyc.utils.server import ThreadedServer

import server
from server.game import auth
from server.game.state import Game
from server.server_runner import Server


def save_thread(file: str | None) -> None:
    if file is None:
        file = "backups/state.pickle"

    state = server.game_state

    with tempfile.NamedTemporaryFile(delete=False) as f:
        dill.dump(state, f)

        os.rename(f.name, file)

    logging.info(msg=f"Backup saved in {file}")


def debug_server(path: str):
    server = ThreadedServer(service=SlaveService, auto_register=False, socket_path=path)
    import threading

    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()


def run() -> None:
    # tracer = VizTracer(
    #     log_async=True, tracer_entries=10000000, output_file="result.json"
    # )
    # tracer.enable_thread_tracing()
    # tracer.start()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-p", "--port", help="Port Default 1337", default=1337)
    parser.add_argument("--host", help="Host Default 0.0.0.0", default="0.0.0.0")
    parser.add_argument(
        "--backup_file", help="Server backup file and auto restore", default=None
    )
    parser.add_argument("--debug_socket", help="Debug socket for server", default=None)
    parser.add_argument("--auth_path", help="Path for credentials file", default=None)
    parser.add_argument(
        "--clickhouse_url", help="Clickhouse URL", default="http://localhost:8123/"
    )

    args = parser.parse_args()

    log = logging.getLogger()
    log.handlers.clear()
    log.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    log.addHandler(handler)

    assert args.auth_path, "Auth Path Needed"
    auth.auth_path = args.auth_path

    if args.debug_socket:
        debug_server(args.debug_socket)

    if args.verbose:
        log.setLevel(level=logging.DEBUG)

    server.executor = ProcessPoolExecutor(max_workers=4)

    if args.backup_file and os.path.isfile(args.backup_file):
        with open(args.backup_file, "rb") as f:
            state = cast(Game, dill.load(f))

        state.user_sessions = {}
        state.peer_sessions = {}
        for u in state.users.values():
            u.coords.timestamp = datetime.now()

        server.game_state = state
    else:
        server.game_state = Game()

    server.global_server = Server(args.clickhouse_url)

    log.info(f"Listening on {args.host}:{args.port}")

    running = Event()
    running.set()

    loop = get_event_loop()
    server_coro = server.global_server.start(
        host=args.host, port=args.port, running=running
    )

    # Backups are now done via db
    # save_timer = RepeatedTimer(
    #     interval=60,
    #     function=save_thread,
    #     file=args.backup_file,
    # )
    # save_timer.start()

    try:
        server_task = loop.run_until_complete(server_coro)

        loop.run_forever()
    except KeyboardInterrupt:
        pass

    print("BYE")

    # tracer.stop()
    # tracer.save()
    # Close the server
    server_task.close()  # type: ignore
    loop.run_until_complete(server_task.wait_closed())  # type: ignore
    loop.close()

    running.clear()
    # save_timer.stop()


def debug():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug_socket", help="Debug socket for server", default=None)

    args = parser.parse_args()

    assert args.debug_socket

    from rpyc.utils.classic import unix_connect  # type: ignore

    conn = unix_connect(args.debug_socket)  # type: ignore
    modules = conn.modules  # type: ignore
    from IPython.terminal.embed import embed  # type: ignore

    server = modules["server"]  # type: ignore

    embed(local_ns=locals(), colors="neutral")


if __name__ == "__main__":
    run()
