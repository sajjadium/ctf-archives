from dataclasses import dataclass


@dataclass
class Request:
    method: str
    path: str
    data: str

class InvalidRequest(Exception):
    pass

class MethodNotAllowed(Exception):
    pass