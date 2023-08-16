import asyncio
import time
from asyncio import get_running_loop
from time import sleep as time_sleep

import pyglet

import client
from shared.constants import TARGET_FPS, TARGET_UPS

if pyglet.compat_platform in ["win32", "cygwin"]:

    async def sleep(delay: float):
        await get_running_loop().run_in_executor(None, time_sleep, delay)

else:
    sleep = asyncio.sleep  # type: ignore


async def check_wait() -> None:
    start_lock = time.time()

    tmp_time = time.time()
    while (
        client.game_state.update_lock.locked()
        or (tmp_time - client.game_state.update_lock.t1)
        > client.game_state.update_lock.frequency
    ) and tmp_time - start_lock < (1 / TARGET_UPS) * 2:
        await sleep(((1 / TARGET_UPS) * 0.2))
        tmp_time = time.time()

    start_lock = time.time()
    tmp_time = time.time()
    while (
        (
            client.game_state.draw_lock.locked()
            or tmp_time - client.game_state.draw_lock.t1
        )
        > client.game_state.draw_lock.frequency
    ) and tmp_time - start_lock < (1 / TARGET_FPS) * 2:
        await sleep((1 / TARGET_FPS) * 0.2)
        tmp_time = time.time()
