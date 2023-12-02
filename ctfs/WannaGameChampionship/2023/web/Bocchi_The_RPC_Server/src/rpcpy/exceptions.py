from __future__ import annotations

from baize.exceptions import HTTPException


class SerializerNotFound(Exception):
    """
    Serializer not found
    """


class CallbackError(HTTPException[str]):
    """
    Callback error
    """


class RemoteCallError(Exception):
    """
    Remote call error
    """
