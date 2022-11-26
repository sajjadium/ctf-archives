import logging
import os
import random
import sqlite3
import string

import glacier_webserver.api
import glacier_webserver.config
import glacier_webserver.routes
import glacier_webserver.utils
import jwt
from glacier_webserver.config import app
from glacier_webserver.utils import Database


def prepair_environment():
    secret = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        )
        for _ in range(30)
    )

    admin_jwt = jwt.encode(
        {
            "name": "admin",
            "is_admin": True
        },
        secret,
        algorithm="HS256"
    )

    logging.info(admin_jwt)
    Database().setup_database(admin_jwt)


def main():
    app.before_first_request(prepair_environment)
    app.run(host='0.0.0.0', port='8080')
    return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    raise SystemExit(main())
