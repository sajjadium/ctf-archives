import sqlite3
from functools import wraps
import os

import flask
from flask import redirect
from flask import render_template
from flask import request
from glacier_webserver.config import app


class Filter:
    BAD_URL_SCHEMES = ['file', 'ftp', 'local_file']
    BAD_HOSTNAMES = ["google", "twitter", "githubusercontent", "microsoft"]

    @staticmethod
    def isBadUrl(url):
        return Filter.bad_schema(url)

    @staticmethod
    def bad_schema(url):
        scheme = url.split(':')[0]
        return scheme.lower() in Filter.BAD_URL_SCHEMES

    @staticmethod
    def bad_urls(url):
        for hostname in Filter.BAD_HOSTNAMES:
            if hostname in url:
                return True

        return False


def singleton(cls):
    instances = {}
    
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class Database:
    __instance = None

    def __init__(self, database_name="/tmp/glacier.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def setup_database(self, admin_jwt):
        self.cursor.execute(
            "DROP TABLE IF EXISTS secrets"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS secrets (jwt_secret text PRIMARY KEY)"
        )

        if not self.load_secret():
            self.cursor.execute(
                "INSERT INTO secrets VALUES (?)",
                (admin_jwt,)
            )

        self.connection.commit()

        self.token = self.load_secret()[0][0]

    def load_secret(self):
        secret = self.cursor.execute(
            "select jwt_secret from secrets limit 1;"
        ).fetchall()

        return secret

    def get_admin_token(self):
        return self.token


def require_jwt(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None

        if "token" in request.cookies:
            token = request.cookies["token"]
        else:
            return app.make_response(redirect("/"))

        if token == Database().get_admin_token():
            return func(*args, **kwargs)
        else:
            return app.make_response(redirect("/"))

    return decorator


def render_template_with_wrapper(template_path, page):
    if not os.path.isfile("%(root_path)s/templates/%(tmp_path)s%(page)s.html" % {
            "root_path": app.root_path,
            "tmp_path": template_path,
            "page": page
        }
    ):
        return render_template('error/404.html'), 404

    return render_template(
        template_path + '/template.html',
        content=render_template(
            "%(template_path)s%(page)s.html" % {
                "template_path": template_path,
                "page": page
            }
        ),
        js_file="/static/js/%(template_path)s%(page)s.js" % {
            "template_path": template_path,
            "page": page
        }
    )
