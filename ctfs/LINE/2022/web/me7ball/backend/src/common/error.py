class APIError(Exception):
    """Base class for other exceptions"""
    def __init__(self, description,  reason: str):
        self.description = description
        self.reason = reason

class FileNotAllowed(Exception):
    def __init__(self, _file_extension,message="File Not Allowed"):
        self.message = message
        self._file_extension = _file_extension
        super().__init__(self.message)
    def __str__(self):
        return f'{self._file_extension} {self.message}'

class NullParam(Exception):
    def __init__(self,message="Parameter is null"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message}'