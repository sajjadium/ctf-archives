from flask import Flask, render_template, request, session, redirect, url_for

import os
import secrets
from functools import cache
from markdown import markdown
import psycopg2
import urllib.parse

app = Flask(__name__)
app.secret_key = (os.environ.get("SECRET_KEY") or '_5#y2L"F4Q8z\n\xec]/').encode()
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@cache
def get_database_connection():
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_host = "db"

    connection = psycopg2.connect(user=db_user, password=db_password, host=db_host)
    return connection


with app.app_context():
    with open("setup.sql", "r") as f:
        setup_sql = f.read()
    conn = get_database_connection()
    with conn.cursor() as curr:
        curr.execute(setup_sql)
    conn.commit()


@app.after_request
def apply_csp(response):
    if session.get("username") is not None and session.get("password") is not None:
        response.headers[
            "Content-Security-Policy"
        ] = "default-src 'self'; img-src *; font-src https://fonts.gstatic.com https://fonts.googleapis.com; style-src 'self' https://fonts.googleapis.com"
    return response


@app.get("/")
@app.get("/index")
@app.get("/home")
def index():
    query = request.args.get("search")

    conn = get_database_connection()
    with conn.cursor() as curr:
        if query is None:
            curr.execute("SELECT * FROM ctfers WHERE searchable LIMIT 10 OFFSET 0")
        else:
            curr.execute(
                "SELECT * FROM ctfers WHERE searchable AND (name ILIKE %s OR team ILIKE %s OR specialty ILIKE %s OR description ILIKE %s) LIMIT 10 OFFSET 0",
                [f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"],
            )
        ctfers = curr.fetchall()
    return render_template("index.html", ctfers=ctfers, query=query)


@app.post("/search")
def search():
    search = request.form.get("search")
    return redirect("/?search=" + urllib.parse.quote_plus(search))


@app.get("/login")
def login_page():
    if session.get("username") is not None and session.get("password") is not None:
        return redirect("/")

    error = request.args.get("error")
    return render_template("login.html", error=error)


@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username is None or password is None:
        return redirect(
            "/login?error="
            + urllib.parse.quote_plus("Need both username and password.")
        )

    session["username"] = username
    session["password"] = password

    return redirect("/")


@app.get("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect("/")


@app.get("/view/<pid>")
def page(pid):
    if session.get("username") is not None and session.get("password") is not None:
        return redirect("/edit/{}".format(pid))

    if pid is None:
        return redirect(
            "/404?error=" + urllib.parse.quote_plus("Need to specify a pid.")
        )

    conn = get_database_connection()
    with conn.cursor() as curr:
        curr.execute(
            "SELECT name,image,team,specialty,website,description FROM ctfers WHERE id=%s LIMIT 1",
            [pid],
        )
        ctfer = curr.fetchone()

    if ctfer is None:
        return redirect("/404?error=" + urllib.parse.quote_plus("CTFer not found."))

    (name, image, team, specialty, website, description) = ctfer
    content = markdown(description)
    return render_template(
        "view.html",
        name=name,
        image=image,
        team=team,
        specialty=specialty,
        website=website,
        description=content,
    )


@app.get("/edit/<pid>")
def edit_page(pid):
    if session.get("username") is None or session.get("password") is None:
        return redirect("/view/{}".format(pid))

    conn = get_database_connection()
    with conn.cursor() as curr:
        curr.execute(
            "SELECT id,name,image,team,specialty,website,description,searchable FROM ctfers WHERE id=%s LIMIT 1",
            [pid],
        )
        ctfer = curr.fetchone()

    if ctfer is None:
        return redirect("/create?error=" + urllib.parse.quote_plus("CTFer not found."))

    (id, name, image, team, specialty, website, description, searchable) = ctfer
    return render_template(
        "edit.html",
        id=id,
        name=name,
        image=image,
        team=team,
        specialty=specialty,
        website=website,
        description=description,
        searchable=searchable,
        pid=pid,
    )


@app.post("/edit/<pid>")
def edit_api(pid):
    if session.get("username") is None or session.get("password") is None:
        return redirect("/view/{}".format(pid))

    title = request.form.get("name")
    image = request.form.get("image")
    team = request.form.get("team")
    specialty = request.form.get("specialty")
    website = request.form.get("website")
    description = request.form.get("description")
    searchable = request.form.get("searchable") == "on"

    if (
        title is None
        or image is None
        or team is None
        or specialty is None
        or website is None
        or description is None
    ):
        return redirect(
            "/edit/{}?error=".format(pid) + urllib.parse.quote_plus("Need all fields.")
        )

    conn = get_database_connection()
    with conn.cursor() as curr:
        curr.execute(
            "UPDATE ctfers SET name=%s, image=%s, team=%s, specialty=%s, website=%s, description=%s, searchable=%s WHERE id=%s",
            [title, image, team, specialty, website, description, searchable, pid],
        )
    return redirect("/view/{}".format(pid))


@app.get("/create")
def new_page():
    error = request.args.get("error")
    return render_template("create.html", error=error)


@app.post("/create")
def create_page():
    title = request.form.get("name")
    image = request.form.get("image")
    team = request.form.get("team")
    specialty = request.form.get("specialty")
    website = request.form.get("website")
    description = request.form.get("description")
    searchable = request.form.get("searchable") == "on"

    if (
        title is None
        or image is None
        or team is None
        or specialty is None
        or website is None
        or description is None
    ):
        return redirect("/create?error=" + urllib.parse.quote_plus("Need all fields."))

    conn = get_database_connection()
    with conn.cursor() as curr:
        id = secrets.token_hex(16)
        curr.execute("SELECT id FROM ctfers WHERE id = %s", [id])

        while curr.fetchone() is not None:
            id = secrets.token_hex(16)
            curr.execute("SELECT id FROM ctfers WHERE id = %s", [id])

        curr.execute(
            "INSERT INTO ctfers (id, name, image, team, specialty, website, description, searchable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            [id, title, image, team, specialty, website, description, searchable],
        )
        id = curr.fetchone()[0]

    return redirect("/view/{}".format(id))


@app.delete("/delete/<pid>")
def delete_page(pid):
    if session.get("username") is None or session.get("password") is None:
        return redirect("/login?error=" + urllib.parse.quote_plus("Not logged in."))

    conn = get_database_connection()
    with conn.cursor() as curr:
        curr.execute("DELETE FROM ctfers WHERE id = %s", [pid])
    return redirect("/")


@app.post("/flag")
def flag():
    adminpw = os.environ.get("ADMINPW") or "admin"
    if session.get("password") != adminpw:
        return redirect("/login?error=" + urllib.parse.quote_plus("Not the admin."))

    flag = os.environ.get("FLAG") or "lactf{test-flag}"
    return flag, 200


@app.errorhandler(404)
def page_not_found(_):
    error = request.args.get("error") or "Page not found"
    return render_template("404.html", error=error), 404
