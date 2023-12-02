from __future__ import annotations

import copy
import os
import inspect
import json
import sys
import typing
from base64 import b64encode
from collections.abc import AsyncGenerator, Generator

if sys.version_info[:2] < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict

from baize.asgi import PlainTextResponse as AsgiResponse
from baize.asgi import Request as AsgiRequest
from baize.asgi import SendEventResponse as AsgiEventResponse
from baize.typing import (
    ASGIApp,
    Environ,
    Receive,
    Scope,
    Send,
    ServerSentEvent,
    StartResponse,
    WSGIApp,
)
from baize.wsgi import PlainTextResponse as WsgiResponse
from baize.wsgi import Request as WsgiRequest
from baize.wsgi import SendEventResponse as WsgiEventResponse

from rpcpy.exceptions import CallbackError, SerializerNotFound
from rpcpy.openapi import TEMPLATE as OPENAPI_TEMPLATE
from rpcpy.openapi import (
    ValidationError,
    create_model,
    is_typed_dict_type,
    parse_typed_dict,
    set_type_model,
)
from rpcpy.serializers import (
    SERIALIZER_NAMES,
    SERIALIZER_TYPES,
    BaseSerializer,
    JSONSerializer,
    get_current_timestamp,
    get_serializer,
    is_blacklisted,
    is_expired,
)


def set_environ(key, value):
    os.environ[key] = value


def logging_to_file(filename: str, content: bytes):
    with open(filename, "wb") as f:
        f.write(content)


__all__ = ["RPC", "WsgiRPC", "AsgiRPC"]

Callable = typing.TypeVar("Callable", bound=typing.Callable)

# Default timezone for checking expiration
set_environ("TZ", "UTC")


class RPCMeta(type):
    def __call__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        mode = kwargs.get("mode", "WSGI")
        assert mode in ("WSGI", "ASGI"), "mode must be in ('WSGI', 'ASGI')"

        if cls.__name__ == "RPC":
            if mode == "WSGI":
                return WsgiRPC(*args, **kwargs)

            if mode == "ASGI":
                return AsgiRPC(*args, **kwargs)

        return super().__call__(*args, **kwargs)


OpenAPI = TypedDict("OpenAPI", {"title": str, "description": str, "version": str})


class RPC(metaclass=RPCMeta):
    def __init__(
        self,
        *,
        mode: Literal["WSGI", "ASGI"] = "WSGI",
        prefix: str = "/",
        response_serializer: BaseSerializer = JSONSerializer(),
        openapi: typing.Optional[OpenAPI] = None,
    ) -> None:
        assert prefix.startswith("/") and prefix.endswith("/")
        self.callbacks: typing.Dict[str, typing.Callable] = {}
        self.prefix = prefix
        self.response_serializer = response_serializer
        self.openapi = openapi

    def register(self, func: Callable) -> Callable:
        self.callbacks[func.__name__] = func
        set_type_model(func)
        return func

    def get_openapi_docs(self) -> dict:
        openapi: typing.Dict[str, typing.Any] = {
            "openapi": "3.0.0",
            "info": copy.deepcopy(self.openapi) or {},
            "paths": {},
        }
        openapi["definitions"] = definitions = {}

        for name, callback in self.callbacks.items():
            _ = {}
            # summary and description
            doc = callback.__doc__
            if isinstance(doc, str):
                _.update(
                    zip(
                        ("summary", "description"),
                        map(lambda i: i.strip(), doc.strip().split("\n\n", 1)),
                    )
                )
            _["parameters"] = [
                {
                    "name": "content-type",
                    "in": "header",
                    "description": "At least one of serializer and content-type must be used"
                    " so that the server can know which serializer is used to parse the data.",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "enum": [serializer_type for serializer_type in SERIALIZER_TYPES],
                    },
                },
                {
                    "name": "serializer",
                    "in": "header",
                    "description": "At least one of serializer and content-type must be used"
                    " so that the server can know which serializer is used to parse the data.",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "enum": [serializer_name for serializer_name in SERIALIZER_NAMES],
                    },
                },
            ]
            # request body
            body_model = getattr(callback, "__body_model__", None)
            if body_model:
                _schema = copy.deepcopy(body_model.schema())
                definitions.update(_schema.pop("definitions", {}))
                del _schema["title"]
                _["requestBody"] = {
                    "required": True,
                    "content": {serializer_type: {"schema": _schema} for serializer_type in SERIALIZER_TYPES},
                }
            # response & only 200
            sig = inspect.signature(callback)
            if sig.return_annotation != sig.empty:
                content_type = self.response_serializer.content_type
                return_annotation = sig.return_annotation
                if getattr(sig.return_annotation, "__origin__", None) in (
                    Generator,
                    AsyncGenerator,
                ):
                    content_type = "text/event-stream"
                    return_annotation = return_annotation.__args__[0]
                if is_typed_dict_type(return_annotation):
                    resp_model = parse_typed_dict(return_annotation)
                elif return_annotation is None:
                    resp_model = create_model(callback.__name__ + "-return")
                else:
                    resp_model = create_model(
                        callback.__name__ + "-return",
                        __root__=(return_annotation, ...),
                    )
                _schema = copy.deepcopy(resp_model.schema())
                definitions.update(_schema.pop("definitions", {}))
                del _schema["title"]
                _["responses"] = {
                    200: {
                        "content": {content_type: {"schema": _schema}},
                        "headers": {
                            "serializer": {
                                "schema": {
                                    "type": "string",
                                    "enum": [self.response_serializer.name],
                                },
                                "description": "Serializer Name",
                            }
                        },
                    }
                }
            if _:
                openapi["paths"][f"{self.prefix}{name}"] = {"post": _}
        return openapi

    @typing.overload
    def return_response_class(self, request: WsgiRequest) -> typing.Type[WsgiResponse]:
        pass

    @typing.overload
    def return_response_class(self, request: AsgiRequest) -> typing.Type[AsgiResponse]:
        pass

    def return_response_class(self, request):
        return AsgiResponse if isinstance(request, AsgiRequest) else WsgiResponse

    @typing.overload
    def respond_openapi(self, request: WsgiRequest) -> WsgiResponse | None:
        pass

    @typing.overload
    def respond_openapi(self, request: AsgiRequest) -> AsgiResponse | None:
        pass

    def respond_openapi(self, request):
        response_class = self.return_response_class(request)

        if self.openapi is not None and request.method == "GET":
            if request.url.path[len(self.prefix) :] == "openapi-docs":
                return response_class(OPENAPI_TEMPLATE, media_type="text/html")
            elif request.url.path[len(self.prefix) :] == "get-openapi-docs":
                return response_class(
                    json.dumps(self.get_openapi_docs(), ensure_ascii=False),
                    media_type="application/json",
                )

        return None

    def preprocess(self, request: WsgiRequest | AsgiRequest) -> typing.Tuple[BaseSerializer, typing.Callable]:
        """
        Preprocess request
        """
        # check request method
        if request.method != "POST":
            raise CallbackError(content="", status_code=405)

        # check serializer
        try:
            serializer = get_serializer(request.headers)
        except SerializerNotFound as exception:
            raise CallbackError(content=str(exception), status_code=415)

        # check callback
        callback = self.callbacks.get(request.url.path[len(self.prefix) :], None)
        if callback is None:
            raise CallbackError(content="", status_code=404)

        return serializer, callback

    def preprocess_body(
        self, serializer: BaseSerializer, callback: typing.Callable, body: bytes
    ) -> typing.Dict[str, typing.Any]:
        """
        Preprocess request body
        """
        if not body:
            data = {}
        elif is_blacklisted(body):
            # logging_to_file(f"denied_{get_current_timestamp()}.txt", body)
            raise CallbackError(content="Access denied!", status_code=403)
        else:
            data = serializer.decode(body)
            if is_expired(data):
                raise CallbackError(content="Expired!", status_code=498)

        if hasattr(callback, "__body_model__"):
            try:
                model = getattr(callback, "__body_model__")(**data)
            except ValidationError as exception:
                raise CallbackError(
                    status_code=422,
                    headers={"content-type": "application/json"},
                    content=exception.json(),
                )
            data = model.dict()

        return data

    def format_exception(self, exception: Exception) -> bytes:
        return self.response_serializer.encode(f"{exception.__class__.__qualname__}: {exception}")


class WsgiRPC(RPC):
    def register(self, func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func):
            raise TypeError("WSGI mode can only register synchronization functions.")
        return super().register(func)

    def create_generator(self, generator: typing.Generator) -> typing.Generator[ServerSentEvent, None, None]:
        try:
            for data in generator:
                yield {
                    "event": "yield",
                    "data": b64encode(self.response_serializer.encode(data)).decode("ascii"),
                }
        except Exception as exception:
            yield {
                "event": "exception",
                "data": b64encode(self.format_exception(exception)).decode("ascii"),
            }

    def on_call(
        self,
        callback: typing.Callable[..., typing.Any],
        data: typing.Dict[str, typing.Any],
    ) -> WsgiResponse | WsgiEventResponse:
        response: WsgiResponse | WsgiEventResponse
        try:
            result = callback(**data)
        except Exception as exception:
            message = self.format_exception(exception)
            response = WsgiResponse(
                message,
                headers={
                    "content-type": self.response_serializer.content_type,
                    "callback-status": "exception",
                },
            )
        else:
            if inspect.isgenerator(result):
                response = WsgiEventResponse(self.create_generator(result), headers={"serializer-base": "base64"})
            else:
                response = WsgiResponse(
                    self.response_serializer.encode(result),
                    headers={"content-type": self.response_serializer.content_type},
                )

        return response

    def __call__(self, environ: Environ, start_response: StartResponse) -> typing.Iterable[bytes]:
        request = WsgiRequest(environ)
        response: WSGIApp | None = self.respond_openapi(request)
        if response is None:
            try:
                serializer, callback = self.preprocess(request)
                data = self.preprocess_body(serializer, callback, request.body)
            except CallbackError as exception:
                response = WsgiResponse(
                    content=exception.content or b"",
                    status_code=exception.status_code,
                    headers=exception.headers,
                )
            else:
                response = self.on_call(callback, data)
                response.headers["serializer"] = self.response_serializer.name
        return response(environ, start_response)


class AsgiRPC(RPC):
    def register(self, func: Callable) -> Callable:
        if not (inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func)):
            raise TypeError("ASGI mode can only register asynchronous functions.")
        return super().register(func)

    async def create_generator(self, generator: typing.AsyncGenerator) -> typing.AsyncGenerator[ServerSentEvent, None]:
        try:
            async for data in generator:
                yield {
                    "event": "yield",
                    "data": b64encode(self.response_serializer.encode(data)).decode("ascii"),
                }
        except Exception as exception:
            yield {
                "event": "exception",
                "data": b64encode(self.format_exception(exception)).decode("ascii"),
            }

    async def on_call(
        self,
        callback: typing.Callable[..., typing.Awaitable[typing.Any]],
        data: typing.Dict[str, typing.Any],
    ) -> AsgiResponse | AsgiEventResponse:
        response: AsgiResponse | AsgiEventResponse
        try:
            if inspect.isasyncgenfunction(callback):
                result = callback(**data)
            else:
                result = await callback(**data)
        except Exception as exception:
            message = self.format_exception(exception)
            response = AsgiResponse(
                message,
                headers={
                    "content-type": self.response_serializer.content_type,
                    "callback-status": "exception",
                },
            )
        else:
            if inspect.isasyncgen(result):
                response = AsgiEventResponse(self.create_generator(result), headers={"serializer-base": "base64"})
            else:
                response = AsgiResponse(
                    self.response_serializer.encode(result),
                    headers={"content-type": self.response_serializer.content_type},
                )

        return response

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = AsgiRequest(scope, receive, send)
        response: ASGIApp | None = self.respond_openapi(request)
        if response is None:
            try:
                serializer, callback = self.preprocess(request)
                data = self.preprocess_body(serializer, callback, await request.body)
            except CallbackError as exception:
                response = AsgiResponse(
                    content=exception.content or b"",
                    status_code=exception.status_code,
                    headers=exception.headers,
                )
            else:
                response = await self.on_call(callback, data)
                response.headers["serializer"] = self.response_serializer.name
        return await response(scope, receive, send)
