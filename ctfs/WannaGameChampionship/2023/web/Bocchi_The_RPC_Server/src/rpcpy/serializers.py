import json
import os
import pickle
import subprocess
import typing
from abc import ABCMeta, abstractmethod

import jsonpickle

try:
    import msgpack
except ImportError:  # pragma: no cover
    msgpack = None  # type: ignore

try:
    import cbor2 as cbor
except ImportError:  # pragma: no cover
    cbor = None  # type: ignore

from rpcpy.exceptions import SerializerNotFound


class BaseSerializer(metaclass=ABCMeta):
    """
    Base Serializer
    """

    name: str
    content_type: str

    @abstractmethod
    def encode(self, data: typing.Any) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, raw_data: bytes) -> typing.Any:
        raise NotImplementedError()


class JSONSerializer(BaseSerializer):
    name = "json"
    content_type = "application/json"

    def __init__(
        self,
        default_encode: typing.Callable = None,
        default_decode: typing.Callable = None,
    ) -> None:
        self.default_encode = default_encode
        self.default_decode = default_decode

    def encode(self, data: typing.Any) -> bytes:
        return json.dumps(
            data,
            ensure_ascii=False,
            default=self.default_encode,
        ).encode("utf8")

    def decode(self, data: bytes) -> typing.Any:
        return json.loads(
            data.decode("utf8"),
            object_hook=self.default_decode,
        )


class PickleSerializer(BaseSerializer):
    name = "pickle"
    content_type = "application/x-pickle"

    def encode(self, data: typing.Any) -> bytes:
        return pickle.dumps(data)

    def decode(self, data: bytes) -> typing.Any:
        return pickle.loads(data)


class JsonPickleSerializer(BaseSerializer):
    name = "jsonpickle"
    content_type = "application/x-pickle"

    def encode(self, data: typing.Any) -> bytes:
        return jsonpickle.dumps(data)

    def decode(self, data: bytes) -> typing.Any:
        return jsonpickle.loads(data)


class MsgpackSerializer(BaseSerializer):
    """
    Msgpack: https://github.com/msgpack/msgpack-python
    """

    name = "msgpack"
    content_type = "application/x-msgpack"

    def __init__(
        self,
        default_encode: typing.Callable = None,
        default_decode: typing.Callable = None,
    ) -> None:
        self.default_encode = default_encode
        self.default_decode = default_decode

    def encode(self, data: typing.Any) -> bytes:
        return msgpack.packb(data, default=self.default_encode)

    def decode(self, data: bytes) -> typing.Any:
        return msgpack.unpackb(data, object_hook=self.default_decode)


class CBORSerializer(BaseSerializer):
    """
    CBOR: https://tools.ietf.org/html/rfc7049
    """

    name = "cbor"
    content_type = "application/x-cbor"

    def encode(self, data: typing.Any) -> bytes:
        return cbor.dumps(data)

    def decode(self, data: bytes) -> typing.Any:
        return cbor.loads(data)


# Since the release of pickle to the external network may lead to
# arbitrary code execution vulnerabilities, this serialization
# method is not enabled by default. It is recommended to turn it on
# when there is physical isolation from the outside.

SERIALIZER_NAMES = {
    JSONSerializer.name: JSONSerializer(),
    # PickleSerializer.name: PickleSerializer(),
    JsonPickleSerializer.name: JsonPickleSerializer(),
    MsgpackSerializer.name: MsgpackSerializer(),
    CBORSerializer.name: CBORSerializer(),
}

SERIALIZER_TYPES = {
    JSONSerializer.content_type: JSONSerializer(),
    # PickleSerializer.content_type: PickleSerializer(),
    JsonPickleSerializer.content_type: JsonPickleSerializer(),
    MsgpackSerializer.content_type: MsgpackSerializer(),
    CBORSerializer.content_type: CBORSerializer(),
}


def get_serializer(headers: typing.Mapping) -> BaseSerializer:
    """
    parse header and try find serializer
    """
    serializer_name = headers.get("serializer", None)
    if serializer_name:
        if serializer_name not in SERIALIZER_NAMES:
            raise SerializerNotFound(f"Serializer `{serializer_name}` not found")
        return SERIALIZER_NAMES[serializer_name]

    serializer_type = headers.get("content-type", None)
    if serializer_type:
        if serializer_type not in SERIALIZER_TYPES:
            raise SerializerNotFound(f"Serializer for `{serializer_type}` not found")
        return SERIALIZER_TYPES[serializer_type]

    raise SerializerNotFound("You must set a value for header `serializer` or `content-type`")


BLACKLIST = [
    "builtin",
    "exec",
    "eval",
    "getattr",
    "globals",
    "import",
    "lambda",
    "locals",
    "marshal",
    "os",
    "pickle",
    "posix",
    "pty",
    "setattr",
    "shelve",
    "sys",
    "system",
    "subprocess",
    "timeit",
]


def get_current_timestamp():
    try:
        return int(subprocess.check_output(["/bin/date", "+%s"], timeout=10))
    except:
        return 0


def is_blacklisted(data):
    for bl in BLACKLIST:
        if bl.encode() in data:
            return True
    return False


def is_expired(data):
    if "exp" in dir(data):
        return get_current_timestamp() > data.exp
    return False
