import codecs
import csv
import os
import sqlite3
import time
import threading
import traceback
import uuid
from collections import deque
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

DATABASE_EXPIRY_TIME = 5 * 60
DEMO_QUERY_LIMIT = 2
DEMO_ROW_LIMIT = 200


def quote_identifier(s, errors="strict"):
    # https://stackoverflow.com/questions/6514274/how-do-you-escape-strings-for-sqlite-table-column-names-in-python
    encodable = s.encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError(
            "NUL-terminated utf-8",
            encodable,
            nul_index,
            nul_index + 1,
            "NUL not allowed",
        )
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return '"' + encodable.replace('"', '""') + '"'


def convert_value(v: str) -> Any:
    try:
        return int(v)
    except Exception:
        pass

    try:
        return float(v)
    except Exception:
        pass

    return v


def format_filter(filt: tuple[str, str, str]) -> str:
    col_name, operator, _ = filt
    assert operator.upper() in (
        "<",
        ">",
        "<=",
        ">=",
        "=",
        "==",
        "<>",
        "!=",
        "IS",
        "IS NOT",
        "LIKE",
        "NOT LIKE",
    )
    return "%s %s ?" % (quote_identifier(col_name), operator)


def format_order(order: tuple[str, str]) -> str:
    col_name, direction = order
    assert direction.upper() in ["ASC", "DESC"]
    return "%s %s" % (quote_identifier(col_name), direction)


class Database:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")

    def create_table(self, table_name: str, column_names: list[str]) -> None:
        self.db.execute(
            "CREATE TABLE %s (%s)"
            % (
                quote_identifier(table_name),
                ", ".join(quote_identifier(col) for col in column_names),
            )
        )

    def insert_row(self, table_name: str, values: list[str]) -> None:
        self.db.execute(
            "INSERT INTO %s VALUES (%s)" % (quote_identifier(table_name), ", ".join(["?"] * len(values))),
            values,
        )

    def select_from(
        self,
        table_name: str,
        filters: list[tuple[str, str, str]],
        orders: list[tuple[str, str]],
    ) -> list[tuple[Any, ...]]:
        query = "SELECT * FROM %s" % quote_identifier(table_name)
        params = []
        if filters:
            query += " WHERE %s" % " AND ".join(format_filter(f) for f in filters)
            params = [convert_value(f[2]) for f in filters]
        if orders:
            query += " ORDER BY %s" % ", ".join(format_order(f) for f in orders)
        return self.db.execute(query, params).fetchall()


@dataclass
class Table:
    expiry_time: float
    queries_left: int
    col_names: str
    database: Database
    lock: threading.Lock


table_list: list[str] = deque()
tables: dict[str, Table] = {}


@app.route("/upgrade/<uuid:table_id>", methods=["POST"])
def upgrade(table_id: str):
    if "key" not in request.form or not request.form["key"]:
        flash("No license key provided")
        return redirect(url_for("view", table_id=table_id))

    table = tables.get(table_id, None)
    if not table:
        flash("Table expired or does not exist")
        return redirect(url_for("index"))

    with table.lock:
        keys = table.database.select_from("license", [("key", "==", request.form["key"])], [])
        if not keys:
            flash("Invalid license key")
            return redirect(url_for("view", table_id=table_id))

    return render_template("upgrade.html", flag=os.environ.get("FLAG", "no flag found - contact admin!"))


@app.route("/view/<uuid:table_id>", methods=["GET", "POST"])
def view(table_id: str):
    table = tables.get(table_id, None)
    if not table:
        flash("Table expired or does not exist")
        return redirect(url_for("index"))

    operations = {
        # value: (html, sql)
        "eq": ("=", "="),
        "ne": ("≠", "!="),
        "lt": ("<", "<"),
        "gt": (">", ">"),
        "le": ("≤", "<="),
        "ge": ("≥", ">="),
        "like": ("like", "LIKE"),
        "unlike": ("unlike", "NOT LIKE"),
    }

    if request.method == "POST":
        filters = list(
            zip(
                request.form.getlist("filter-col"),
                request.form.getlist("filter-op"),
                request.form.getlist("filter-val"),
            )
        )
        db_filters = [(col_name, operations[op][1], value) for col_name, op, value in filters]

        orders = list(zip(request.form.getlist("order-col"), request.form.getlist("order-od")))
        db_orders = [(col_name, od) for col_name, od in orders]
    else:
        filters = db_filters = []
        orders = db_orders = []

    with table.lock:
        if table.queries_left > 0:
            table.queries_left -= 1

            try:
                data = table.database.select_from("data", db_filters, db_orders)
            except Exception as e:
                flash("Database query failed")
                data = []
        else:
            flash("Your demo has expired!")
            data = []

    return render_template("view.html", **locals())


@app.route("/create", methods=["POST"])
def create():
    if "file" not in request.files:
        flash("No file submitted")
        return redirect(url_for("index"))

    database = Database()

    try:
        file = request.files["file"]
        reader = csv.reader(TextIOWrapper(file))
        fieldnames = next(reader)

        database.create_table("data", fieldnames)
        database.col_names = fieldnames

        for i, row in zip(range(DEMO_ROW_LIMIT), reader):
            database.insert_row("data", [convert_value(v) for v in row[: len(fieldnames)]])

        database.create_table("license", ["key"])
        key = os.urandom(128).hex()
        database.insert_row("license", [key])

    except Exception:
        flash("Unable to parse your input!")
        return redirect(url_for("index"))

    table_id = uuid.uuid4()
    table_list.append(table_id)
    tables[table_id] = Table(
        expiry_time=time.time() + DATABASE_EXPIRY_TIME,
        queries_left=DEMO_QUERY_LIMIT,
        col_names=fieldnames,
        database=database,
        lock=threading.Lock(),
    )

    return redirect(url_for("view", table_id=table_id))


@app.get("/")
def index():
    return render_template("index.html")


def cleanup_thread():
    while 1:
        time.sleep(10)
        try:
            while table_list:
                table_id = table_list[0]
                table = tables.get(table_id, None)
                if table and table.expiry_time > time.time():
                    break
                tables.pop(table_id, None)
                table_list.popleft()
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    threading.Thread(target=cleanup_thread, daemon=True).start()
    app.run()
