import functools
import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from utils import *
from config import cfg


internal_bp = Blueprint('internal', __name__, url_prefix='/internal')


@internal_bp.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    conn = create_connection()
    headers = {
        cfg["HEADER"]["USERNAME"]: data["username"],
        cfg["HEADER"]["PASSWORD"]: data["password"]
    }
    conn.request("GET", "/auth", headers=headers)
    resp = conn.get_response()
    return resp.read()


@internal_bp.route("/health", methods=["POST"])
def health():
    try:
        data = request.get_json()

        if "type" in data.keys():
            if data["type"] == "1.1":
                requests.get("https://" + cfg["INTERNAL"]["HOST"] + "/health", verify=False)

                headers = {
                    cfg["HEADER"]["USERNAME"]: cfg["ADMIN"]["USERNAME"],
                    cfg["HEADER"]["PASSWORD"]: cfg["ADMIN"]["PASSWORD"]
                }
                requests.get("https://" + cfg["INTERNAL"]["HOST"] + "/auth", headers=headers, verify=False)
                r = requests.post("https://" + cfg["INTERNAL"]["HOST"] + "/", data=data["data"].encode('latin-1'), verify=False)
                return r.text

            elif data["type"] == "2":
                conn = create_connection()
                conn.request("GET", "/health")
                resp = conn.get_response()

                headers = {
                    cfg["HEADER"]["USERNAME"]: cfg["ADMIN"]["USERNAME"],
                    cfg["HEADER"]["PASSWORD"]: cfg["ADMIN"]["PASSWORD"]
                }
                conn.request("GET", "/auth", headers=headers)
                resp = conn.get_response()

                conn._new_stream()
                
                conn._send_cb(data["data"].encode('latin-1'))
                conn._sock.fill()
                return conn._sock.buffer.tobytes()
                
            else:
                return "done."
        else:
            return "done."
            
    except:
        return "error occurs"
