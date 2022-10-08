import os

from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, render_template, request, flash, Response
import hashlib
import requests
import base64
import shutil
import time
import string
import random
import json
from subprocess import run, PIPE


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__)


# Sends a generated report on the local file system to an endpoint
@app.route('/send_report', methods=['GET'])
def get_report():
    report_id = request.args.get("report_id")
    target_url = request.args.get("target")
    session_id = request.args.get("session_id")

    report_file = f'output/{report_id}'
    if not os.path.isfile(report_file):
        return Response("ERROR", status=500)

    data = open(report_file, "r").read()

    requests.post(target_url, data=data, params={"report_id":report_id, "session_id":session_id})

    return Response("OK", status=200)

# Generates a report using the provided input arguments
@app.route('/generate_report', methods=['POST'])
def generate():
    data = json.loads(request.data)
    year_start = data["startyear"]
    year_end = data["endyear"]
    country = data["country"].replace("\"", "").replace("'", "")
    report_id = data["report_id"]
    session_id = data["session_id"]

    template = open("data/template.xsl", "r").read()
    template = template.replace("%%COUNTRY%%", country).replace("%%STARTYEAR%%", year_start).replace("%%ENDYEAR%%", year_end)

    try:
        p = run(['./Xalan', '-o', f'output/{report_id}', 'data/population.xml', '-'], stdout=PIPE,
            input=template, encoding='ascii', timeout=3)

        if (p.returncode != 0):
            return Response("ERROR", status=500)
    except:
            return Response("ERROR", status=500)

    return Response("OK", status=200)

    
if __name__ == "__main__":
    app.run()