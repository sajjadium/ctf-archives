import argparse
import asyncio
import logging
import multiprocessing
import sys
import threading
import traceback
from multiprocessing.synchronize import Event as MultiprocessingEventClass

import aioprocessing
import pyglet

import client
from client.game.state import GameState
from client.networking.network import Connection
from client.networking.runner import Runner
from client.scenes.dino_runner import DinoRunner
from client.scenes.game import Game
from client.scenes.game_over import GameOver
from client.scenes.globals import Globals
from client.scenes.intro import Intro
from client.scenes.mainmenu import MainMenu
from client.scenes.scenemanager import SceneManager
from client.scenes.test import TestScene

# from client.scenes.game import Game
from shared.constants import TARGET_FPS, TARGET_UPS


def background_thread(connection: Connection, running: threading.Event) -> None:
    loop = asyncio.new_event_loop()

    async def run() -> None:
        loop_task = loop.create_task(connection.ping_loop(running))
        send_loop_task = loop.create_task(connection.send_message_loop(running))
        message_loop_task = loop.create_task(connection.read_message_loop(running))

        for coro in asyncio.as_completed(
            [loop_task, send_loop_task, message_loop_task]
        ):
            await coro

            running.clear()
            break

    try:
        loop.run_until_complete(run())
    except Exception:
        traceback.print_exc()

    pyglet.app.exit()


def background_process(runner: Runner, running: MultiprocessingEventClass):
    loop = asyncio.new_event_loop()

    async def run() -> None:
        send_loop_task = loop.create_task(runner.send_message_loop(running))
        message_loop_task = loop.create_task(runner.read_message_loop(running))

        for coro in asyncio.as_completed([send_loop_task, message_loop_task]):
            await coro

            running.clear()
            break

    try:
        loop.run_until_complete(run())
    except Exception:
        traceback.print_exc()

    pyglet.app.exit()


def run() -> None:
    # tracer = VizTracer(log_async=True, tracer_entries=10000000, output_file="result.gz")
    # tracer.enable_thread_tracing()
    # tracer.start()
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-p", "--port", help="Port Default 1337", default=1337)
    parser.add_argument("--host", help="Host Default 127.0.0.1", default="127.0.0.1")
    parser.add_argument("--ssl", help="Use ssl", action="store_true")
    parser.add_argument("--username", help="Username prefill", default="")
    parser.add_argument("--password", help="Password prefill", default="")

    args = parser.parse_args()

    log = logging.getLogger()
    log.handlers.clear()
    log.setLevel(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    log.addHandler(handler)

    if args.verbose:
        log.setLevel(level=logging.DEBUG)

    running = threading.Event()
    running.set()

    config = pyglet.gl.Config(
        double_buffer=True,
        depth_size=16,
        major_version=3,
        minor_version=3,
        stencil_size=8,
    )

    window = pyglet.window.Window(width=960, height=544, config=config, vsync=False)
    global_overlay = Globals(window)

    client.game_state = GameState()

    runner_con = aioprocessing.AioQueue()
    thread_con = aioprocessing.AioQueue()

    runner = Runner(
        runner_con=runner_con,
        thread_con=thread_con,
        host=args.host,
        port=args.port,
        ssl=args.ssl,
    )

    client.global_connection = Connection(
        runner_con=runner_con,
        thread_con=thread_con,
        error_handler=global_overlay.on_error,
        game_state=client.game_state,
    )

    client.global_connection.login_handler += client.game_state.login

    client.scene_manager = SceneManager(window)
    scene_manager = client.scene_manager
    pyglet.clock.schedule_interval(scene_manager.update, 1 / TARGET_UPS)

    game = Game(window)
    scene_manager.add_scene("game", game)

    mainmenu = MainMenu(window, args.username, args.password)
    scene_manager.add_scene("mainmenu", mainmenu)

    game_over = GameOver(window)
    scene_manager.add_scene("game_over", game_over)

    intro = Intro(window=window)
    scene_manager.add_scene("intro", intro)

    test = TestScene(window)
    scene_manager.add_scene("test", test)

    scene_manager.add_scene("globals", global_overlay)

    # scene_manager.set_scene("mainmenu")
    scene_manager.set_scene("intro")

    dino_runner = DinoRunner(window)
    scene_manager.add_scene("dino_runner", dino_runner)
    # scene_manager.set_scene("game")
    scene_manager.set_overlay_scene(scene="globals")

    th = threading.Thread(
        target=background_thread, args=[client.global_connection, running]
    )
    th.start()

    process_running = multiprocessing.Event()
    process_running.set()
    p = aioprocessing.AioProcess(
        target=background_process, args=[runner, process_running]
    )
    p.start()  # type: ignore

    try:
        pyglet.app.run(1 / TARGET_FPS)
    except:
        traceback.print_exc()

    print("BEFORE BYE")
    # tracer.stop()
    # print("SAVING")
    # tracer.save()
    # print("SAVED")

    running.clear()
    process_running.clear()
    th.join()
    p.join()  # type: ignore

    print("BYE")


if __name__ == "__main__":
    run()
