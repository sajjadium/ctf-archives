from os import getenv


cfg = {
    "HEADER": {
        "USERNAME": getenv("USERNAME_HEADER"),
        "PASSWORD": getenv("PASSWORD_HEADER")
    },
    "ADMIN": {
        "USERNAME": getenv("USERNAME_ADMIN"),
        "PASSWORD": getenv("PASSWORD_ADMIN")
    },
    "INTERNAL": {
        "HOST": getenv("INTERNAL_HOST")
    }
}