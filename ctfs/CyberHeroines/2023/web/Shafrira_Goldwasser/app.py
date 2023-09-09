from flask import Flask, render_template, request
import sqlite3
import subprocess

app = Flask(__name__)

# Database connection
#DATABASE = "database.db"

def query_database(name):
    query = 'sqlite3 database.db "SELECT biography FROM cyberheroines WHERE name=\'' + str(name) +'\'\"'
    result = subprocess.check_output(query, shell=True, text=True)
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_name = request.form.get("heroine_name")
        biography = query_database(selected_name)
        return render_template("index.html", biography=biography)
    return render_template("index.html", biography="")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')

