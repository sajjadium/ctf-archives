from __future__ import annotations

import functools
import inspect
import typing
from base64 import b64decode

import httpx

from rpcpy.exceptions import RemoteCallError
from rpcpy.openapi import validate_arguments
from rpcpy.serializers import BaseSerializer, JSONSerializer, get_serializer

if typing.TYPE_CHECKING:
    from baize.typing import ServerSentEvent

__all__ = ["Client"]

Callable = typing.TypeVar("Callable", bound=typing.Callable)


class ClientMeta(type):
    def __call__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if cls.__name__ == "Client":
            if isinstance(args[0], httpx.Client):
                return SyncClient(*args, **kwargs)

            if isinstance(args[0], httpx.AsyncClient):
                return AsyncClient(*args, **kwargs)

            raise TypeError(
                "The parameter `client` must be an httpx.Client or httpx.AsyncClient object."
            )

        return super().__call__(*args, **kwargs)


class Client(metaclass=ClientMeta):
    def __init__(
        self,
        client: typing.Union[httpx.Client, httpx.AsyncClient],
        *,
        base_url: str,
        request_serializer: BaseSerializer = JSONSerializer(),
    ) -> None:
        assert base_url.endswith("/"), "base_url must be end with '/'"
        self.base_url = base_url
        self.client = client
        self.request_serializer = request_serializer

    def remote_call(self, func: Callable) -> Callable:
        return func

    def _get_url(self, func: typing.Callable) -> str:
        return self.base_url + func.__name__

    def _get_content(
        self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any
    ) -> bytes:
        sig = inspect.signature(func)
        bound_values = sig.bind(*args, **kwargs)
        parameters = dict(**bound_values.arguments)
        if parameters:
            return self.request_serializer.encode(parameters)
        else:
            return b""


class AsyncClient(Client):
    if typing.TYPE_CHECKING:
        client: httpx.AsyncClient

    def remote_call(self, func: Callable) -> Callable:
        if not (inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func)):
            raise TypeError(
                "Asynchronous Client can only register asynchronous functions."
            )

        func = super().remote_call(func)
        url = self._get_url(func)

        if not inspect.isasyncgenfunction(func):

            @validate_arguments
            @functools.wraps(func)
            async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                post_content = self._get_content(func, *args, **kwargs)
                resp = await self.client.post(
                    url,
                    content=post_content,
                    headers={
                        "content-type": self.request_serializer.content_type,
                        "serializer": self.request_serializer.name,
                    },
                )
                resp.raise_for_status()
                content = get_serializer(resp.headers).decode(resp.content)
                if resp.headers.get("callback-status") == "exception":
                    raise RemoteCallError(content)
                else:
                    return content

        else:

            @validate_arguments
            @functools.wraps(func)
            async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                post_content = self._get_content(func, *args, **kwargs)
                async with self.client.stream(
                    "POST",
                    url,
                    content=post_content,
                    headers={
                        "content-type": self.request_serializer.content_type,
                        "serializer": self.request_serializer.name,
                    },
                ) as resp:
                    resp.raise_for_status()
                    sse_parser = ServerSentEventsParser()
                    serializer = get_serializer(resp.headers)
                    async for line in resp.aiter_lines():
                        event = sse_parser.feed(line)
                        if not event:
                            continue

                        if event["event"] == "yield":
                            yield serializer.decode(
                                b64decode(event["data"].encode("ascii"))
                            )
                        elif event["event"] == "exception":
                            raise RemoteCallError(
                                serializer.decode(b64decode(event["data"].encode("ascii")))
                            )
                        else:
                            raise RuntimeError(f"Unknown event type: {event['event']}")

        return typing.cast(Callable, wrapper)


class SyncClient(Client):
    if typing.TYPE_CHECKING:
        client: httpx.Client

    def remote_call(self, func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func):
            raise TypeError(
                "Synchronization Client can only register synchronization functions."
            )

        func = super().remote_call(func)
        url = self._get_url(func)

        if not inspect.isgeneratorfunction(func):

            @validate_arguments
            @functools.wraps(func)
            def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                post_content = self._get_content(func, *args, **kwargs)
                resp = self.client.post(
                    url,
                    content=post_content,
                    headers={
                        "content-type": self.request_serializer.content_type,
                        "serializer": self.request_serializer.name,
                    },
                )
                resp.raise_for_status()
                content = get_serializer(resp.headers).decode(resp.content)
                if resp.headers.get("callback-status") == "exception":
                    raise RemoteCallError(content)
                else:
                    return content

        else:

            @validate_arguments
            @functools.wraps(func)
            def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                post_content = self._get_content(func, *args, **kwargs)
                with self.client.stream(
                    "POST",
                    url,
                    content=post_content,
                    headers={
                        "content-type": self.request_serializer.content_type,
                        "serializer": self.request_serializer.name,
                    },
                ) as resp:
                    resp.raise_for_status()
                    sse_parser = ServerSentEventsParser()
                    serializer = get_serializer(resp.headers)
                    for line in resp.iter_lines():
                        event = sse_parser.feed(line)
                        if not event:
                            continue

                        if event["event"] == "yield":
                            yield serializer.decode(
                                b64decode(event["data"].encode("ascii"))
                            )
                        elif event["event"] == "exception":
                            raise RemoteCallError(
                                serializer.decode(b64decode(event["data"].encode("ascii")))
                            )
                        else:
                            raise RuntimeError(f"Unknown event type: {event['event']}")

        return typing.cast(Callable, wrapper)


class ServerSentEventsParser:
    def __init__(self) -> None:
        self.message: ServerSentEvent = {}

    def feed(self, line: str) -> ServerSentEvent | None:
        if line == "\n":  # event split line
            event = self.message
            self.message = {}
            return event

        if line[0] == ":":  # ignore comment
            return None

        try:
            key, value = map(str.strip, line.split(":", maxsplit=1))
        except ValueError:
            key = line.strip()
            value = ""

        if key not in ("data", "event", "id", "retry"):  # ignore undefined key
            return None

        if key == "data" and key in self.message:
            self.message["data"] = f'{self.message["data"]}\n{value}'
        elif key == "retry":
            try:
                self.message["retry"] = int(value)
            except ValueError:
                pass  # ignore non-integer retry value
        else:
            self.message[key] = value  # type: ignore[literal-required]

        return None
