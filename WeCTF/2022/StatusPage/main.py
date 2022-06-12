import os
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, jsonify, request

import psutil
from influxdb import InfluxDBClient
from multiprocessing import Process

DB_NAME = "network"


def network_stats():
    return psutil.net_io_counters()._asdict()


def get_conn():
    return InfluxDBClient(host='localhost', port=8086)


def push_stats():
    client = get_conn()
    while True:
        json_body = []
        for k, v in network_stats().items():
            json_body.append({
                "measurement": k,
                "tags": {},
                "time": datetime.utcnow(),
                "fields": {"value": v}
            })
        client.write_points(json_body, database=DB_NAME)
        time.sleep(3)


def initialize():
    client = get_conn()
    client.drop_database(DB_NAME)
    client.create_database(DB_NAME)

    def rand():
        return "a" + str(uuid.uuid4()).replace("-", "")[:9]
    flag_db = rand()
    client.create_database(flag_db)
    client.write_points([{
        "measurement": rand(),
        "tags": {},
        "time": datetime.utcnow(),
        "fields": {"flag": os.getenv("flag")}
    }], database=flag_db)
    Process(target=push_stats, ).start()


measurements = ["bytes_sent", "bytes_recv"]


def get_measurement(minutes):
    results = []
    client = get_conn()
    for db in measurements:
        result = client.query(
            f'SELECT MEAN("value") AS dp FROM "{db}" WHERE time > now() - {minutes}m GROUP BY time(1m)',
            database=DB_NAME
        )
        if type(result) == list:
            return results
        if (db, None) in result.keys():
            for item in result[(db, None)]:
                idx = measurements.index(db)
                if len(results) <= idx:
                    results.append({"x": [], "y": [], "type": "scatter", "name": db})
                results[idx]["x"].append(item["time"] if item["time"] else 0)
                results[idx]["y"].append(item["dp"] if item["dp"] else 0)
    return results


app = Flask(__name__)


@app.route("/q")
def query():
    minutes = request.args.get("minutes")
    return jsonify(get_measurement(minutes if minutes else 10))


@app.route("/")
def index():
    return render_template("index.html")


initialize()
app.run(port=80, host="0.0.0.0")
