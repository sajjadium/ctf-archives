""" Flask Session Cookie Decoder/Encoder """
__author__ = 'Wilson Sumanang, Alexandre ZANNI'

# https://github.com/noraj/flask-session-cookie-manager/blob/master/flask_session_cookie_manager3.py

# standard imports
import sys
import zlib
from itsdangerous import base64_decode
import ast

# external Imports
from flask.sessions import SecureCookieSessionInterface


def cookie_decode(session_cookie_value, secret_key=None):
    """ Decode a Flask cookie  """
    try:
        if(secret_key==None):
            compressed = False
            payload = session_cookie_value

            if payload.startswith('.'):
                compressed = True
                payload = payload[1:]

            data = payload.split(".")[0]

            data = base64_decode(data)
            if compressed:
                data = zlib.decompress(data)

            return data
        else:
            app = MockApp(secret_key)

            si = SecureCookieSessionInterface()
            s = si.get_signing_serializer(app)

            return s.loads(session_cookie_value)
    except Exception as e:
        return "[Decoding error] {}".format(e)
        raise e