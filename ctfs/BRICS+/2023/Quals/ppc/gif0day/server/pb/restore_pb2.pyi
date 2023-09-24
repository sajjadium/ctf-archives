from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Answer(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: str
    def __init__(self, answer: _Optional[str] = ...) -> None: ...

class RestoreRequest(_message.Message):
    __slots__ = ["hash", "salt", "gif"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    SALT_FIELD_NUMBER: _ClassVar[int]
    GIF_FIELD_NUMBER: _ClassVar[int]
    hash: str
    salt: str
    gif: bytes
    def __init__(self, hash: _Optional[str] = ..., salt: _Optional[str] = ..., gif: _Optional[bytes] = ...) -> None: ...
