import os


def getenv(key: str) -> str:
    """Get environment variable and raise an error if it is unset."""
    if val := os.getenv(key):
        return val
    msg = "ENV variable %s is required!"
    raise OSError(msg % key)


IS_DEV = os.getenv("ENV") == "DEV"
