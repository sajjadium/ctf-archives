import base64
import json
import os
import re
import threading
import time
from typing import Annotated

from fastapi import FastAPI, Cookie
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
default_users = {"1_t0taL1y_w4tCh3d_4Un3": base64.b64encode(os.urandom(64)).decode("utf-8"),
                 "SSLv3 enjoyer": base64.b64encode(os.urandom(64)).decode("utf-8"),
                 "HTTP/2 isn't a hypertext protocol": base64.b64encode(os.urandom(64)).decode("utf-8")}
users = default_users.copy()


class Registration(BaseModel):
    username: str
    password: str


@app.post("/admin/register")
def register(user: Registration):
    if not re.match(r"[a-zA-Z]{1,8}", user.username):
        return Response(status_code=400, content="Bad Request")

    users[user.username] = user.password
    return Response(status_code=204)


@app.get("/dashboard")
def dashboard(credentials: Annotated[str | None, Cookie()] = None):
    if not credentials:
        return Response(status_code=401, content="Unauthorized")

    user_info = json.loads(base64.b64decode(credentials))
    if user_info["username"] not in users or user_info["password"] != users[user_info["username"]]:
        return Response(status_code=401, content="Unauthorized")

    with open("static/dashboard.html") as dashboard_file:
        return HTMLResponse(content=dashboard_file.read())


templates = Jinja2Templates(directory="templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"users": ", ".join(users.keys())}
    )


def reset_users():
    global users
    while True:
        users = default_users.copy()
        time.sleep(5 * 60)


reset_thread = threading.Thread(target=reset_users)
reset_thread.start()
