from __future__ import annotations

from asyncio import Lock
from threading import Timer
from typing import Any, Awaitable, Callable, List


class AsyncLockEventHandler(object):
    lock: Lock

    def __init__(
        self, handlers: List[Callable[[Lock, *Any], Awaitable[None]]] | None = None
    ) -> None:
        self.lock = Lock()

        if handlers is None:
            self.__eventhandlers = []
        else:
            self.__eventhandlers = handlers

    def __iadd__(
        self, handler: Callable[[Lock, *Any], Awaitable[None]]
    ) -> AsyncLockEventHandler:
        self.__eventhandlers.append(handler)
        return self

    def __isub__(
        self, handler: Callable[[Lock, *Any], Awaitable[None]]
    ) -> AsyncLockEventHandler:
        self.__eventhandlers.remove(handler)
        return self

    async def __call__(self, *args: Any, **keywargs: Any) -> None:
        for eventhandler in self.__eventhandlers:
            await eventhandler(self.lock, *args, **keywargs)


class AsyncEventHandler(object):
    def __init__(
        self, handlers: List[Callable[..., Awaitable[None]]] | None = None
    ) -> None:
        if handlers is None:
            self.__eventhandlers = []
        else:
            self.__eventhandlers = handlers

    def __iadd__(self, handler: Callable[..., Awaitable[None]]) -> AsyncEventHandler:
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler: Callable[..., Awaitable[None]]) -> AsyncEventHandler:
        self.__eventhandlers.remove(handler)
        return self

    async def __call__(self, *args: Any, **keywargs: Any) -> None:
        for eventhandler in self.__eventhandlers:
            await eventhandler(*args, **keywargs)


class EventHandler(object):
    def __init__(self, handlers: List[Callable[..., None]] | None = None) -> None:
        if handlers is None:
            self.__eventhandlers = []
        else:
            self.__eventhandlers = handlers

    def __iadd__(self, handler: Callable[..., None]) -> EventHandler:
        self.__eventhandlers.append(handler)

        return self

    def __isub__(self, handler: Callable[..., None]) -> EventHandler:
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args: Any, **keywargs: Any) -> None:
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)


class RepeatedTimer(object):
    def __init__(
        self, interval: int, function: Callable[..., None], *args: Any, **kwargs: Any
    ) -> None:
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self) -> None:
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self) -> None:
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self) -> None:
        if self._timer:
            self._timer.cancel()
            self._timer.join()

        self.is_running = False
