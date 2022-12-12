import base64
import json
import logging
import hashlib
import os
import re
import time
from . import helper
from . import globals as __globals__
from .models import User
from .app import Login
from logging.handlers import RotatingFileHandler
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, request, jsonify, redirect

Formats = {
    1: "json",
    2: "apache",
}


def init_routes(app):
    handler = RotatingFileHandler(os.path.join(os.path.dirname(__file__), "logs", "http.log"), maxBytes=50*1024,
                                  backupCount=3)
    http_logger = logging.getLogger("http")
    http_logger.setLevel(logging.DEBUG)
    http_logger.addHandler(handler)

    def cache_key(*args, **kwargs):
        key = request.method + request.path + str(request.query_string) + \
            str(request.data) + request.headers["User-Agent"]
        # hash the key to keep it short
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @Login.user_loader
    def load_user(uid):
        return User.query.filter_by(id=uid).first()

    @Login.unauthorized_handler
    def unauthorized():
        return redirect("/", 302)

    def lang_injection(data):
        def safe(v):
            v = v.replace("&", "&amp;").replace(
                "<", "&lt;").replace(">", "&gt;")
            v = re.sub(r"on\w+\s*=", "forbidden=", v)
            v = re.sub(r"style\s*=", "forbidden=", v)
            return v

        lang = request.headers["Accept-Language"].split(",")[0]
        lang = safe(lang)
        data = data.replace('@LANG@', lang)

        return data

    @app.after_request
    def after_request(response):
        data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "ip": request.remote_addr,
            "user_agent": request.user_agent.string,
            "date_and_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }
        http_logger.debug("%s", json.dumps(data))
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["POST"])
    def login():
        user = request.json.get("user")
        password = request.json.get("password")
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers else request.remote_addr
        success, usr = helper.Manager.check_user(user, password, ip=ip)
        if success:
            login_user(usr)
            return jsonify({"status": "ok"})
        return jsonify({"status": "error"})

    @app.route("/dashboard")
    @login_required
    @__globals__.Cache.cached(timeout=5, make_cache_key=cache_key)
    def dashboard():
        usr = current_user
        return lang_injection(render_template("dashboard.html", user=usr, level=usr.level))

    @app.route("/logout")
    @login_required
    def logout():
        if current_user.is_user:
            logout_user()
            return redirect("/", 302)
        else:
            return redirect("/dashboard", 302)

    @app.route("/static/js/analytics.js")
    @login_required
    @__globals__.Cache.cached(timeout=5, make_cache_key=cache_key)
    def analytics():
        host = request.headers["X-Forwarded-Host"] if "X-Forwarded-Host" in request.headers else request.host
        # remove all ' and " from the host
        host = host.replace("'", "").replace('"', "")
        return render_template("analytics.js", host=host)

    # take parameters from the URL
    @app.route("/api/backup", methods=["GET"])
    @login_required
    def backup():
        if current_user.level == 10:
            file = request.args.get("file")
            seek = int(request.args.get("seek")
                       ) if request.args.get("seek") else 0
            length = int(request.args.get("length")
                         ) if request.args.get("length") else 0
            try:
                with open(os.path.join(os.path.dirname(__file__), "backups", file), "rb") as f:
                    if seek > 0:
                        f.seek(int(seek))
                    if length > 0:
                        data = f.read(int(length))
                    else:
                        data = open(file, "rb").read()
                return jsonify({"status": "ok", "content": base64.b64encode(data).decode()}), 200, \
                    {"Content-Type": "text/plain"}
            except Exception as e:
                return jsonify({"status": "error", "error": str(e)})
        else:
            return jsonify({"status": "error", "error": "you are not allowed to do this"})

    @app.route("/api/miniserver/start", methods=["GET"])
    @login_required
    def start_miniserver():
        if current_user.is_admin:
            pid, port, err = helper.ServerManager.start_miniserver()
            if pid:
                return jsonify({"status": "ok", "pid": pid, "port": port})
            else:
                return jsonify({"status": "error", "msg": str(err)})
        else:
            return jsonify({"status": "error", "msg": "Permission denied"})

    @app.route('/logs')
    def log():
        log_type = request.args["type"] if "type" in request.args else "1"
        fmt = f"{{0[Formats][{log_type}]}}"
        with open(os.path.join(os.path.dirname(__file__), "logs", "http.log"), "r") as f:
            logs = f.read().split("\n")
        if log_type == "1":
            logs = "\n".join(logs)
        else:
            for i in range(0, len(logs)):
                if logs[i] != "":
                    decoded = json.loads(logs[i])
                    logs[i] = f"{decoded['ip']} - - [{decoded['date_and_time']}] \"{decoded['method']} " \
                              f"{decoded['path']} HTTP/1.1\" {decoded['status']} - \"{decoded['user_agent']}\""
            logs = "\n".join(logs)
        return render_template("log.html", log_type=fmt.format(globals()), log_types=Formats, log_lines=logs)
