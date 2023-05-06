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
from xhtml2pdf import pisa 

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__)


# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err


# Converts HTML content to PDF
@app.route('/render_report', methods=['POST'])
def render_report():
    html_report = request.data.decode()
    session_id = request.args.get("session_id")
    report_id = request.args.get("report_id")
    if len(session_id) < 20:
        return Response("Invalid session", 500)
    
    final_report_id = f"output/{report_id}_{session_id}.pdf"

    convert_html_to_pdf(html_report, final_report_id)

    return Response("OK", 200)

# Reads a generated report from the local file system
@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get("report_id")
    session_id = request.args.get("session_id")

    filename = f"output/{report_id}_{session_id}.pdf"
    if os.path.exists(filename):
        return Response(open(filename, "rb").read(), status=200) 
    
    return Response("Not found", 404)
    
if __name__ == "__main__":
    app.run()