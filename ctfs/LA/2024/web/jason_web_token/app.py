from pathlib import Path

from fastapi import Cookie, FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import auth

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

flag = (Path(__file__).parent / "flag.txt").read_text()
index_html = lambda: (Path(__file__).parent / "index.html").read_text()


class LoginForm(BaseModel):
    username: str
    age: int


@app.post("/login")
def login(login: LoginForm, resp: Response):
    age = login.age
    username = login.username

    if age < 10:
        resp.status_code = 400
        return {"msg": "too young! go enjoy life!"}
    if 18 <= age <= 22:
        resp.status_code = 400
        return {"msg": "too many college hackers, no hacking pls uwu"}

    is_admin = username == auth.admin.username and age == auth.admin.age
    token = auth.create_token(
        username=username,
        age=age,
        role=("admin" if is_admin else "user")
    )

    resp.set_cookie("token", token)
    resp.status_code = 200
    return {"msg": "login successful"}


@app.get("/img")
def img(resp: Response, token: str | None = Cookie(default=None)):
    userinfo, err = auth.decode_token(token)
    if err:
        resp.status_code = 400
        return {"err": err}
    if userinfo["role"] == "admin":
        return {"msg": f"Your flag is {flag}", "img": "/static/bplet.png"}
    return {"msg": "Enjoy this jason for your web token", "img": "/static/aplet.png"}


@app.get("/", response_class=HTMLResponse)
def index():
    return index_html()
