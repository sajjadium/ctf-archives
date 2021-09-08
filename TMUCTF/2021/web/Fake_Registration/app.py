import os
from flask import Flask, render_template, request
from peewee import *

app = Flask(__name__)
db = SqliteDatabase("TMUCTF.db")


class Users(Model):
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


@db.connection_context()
def initialize():
    try:
        db.create_tables([Users])
        Users.create(username="admin", password=os.getenv("FLAG"))
    except:
        pass


initialize()


@app.route("/")
@app.route("/register", methods=["POST"])
def register():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 67:
            msg = "Error: Too long username!"
        elif len(password) > 67:
            msg = "Error: Too long password!"
        else:
            sql = f"INSERT INTO `users`(username, password) VALUES ('{username}', '{password}')"
            try:
                db.execute_sql(sql)
                msg = "Your registration was successful!"
            except Exception as e:
                msg = "Error: " + str(e)
    return render_template("register.html", msg=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
