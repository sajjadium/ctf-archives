import os

from werkzeug.utils import secure_filename
from flask import Flask, redirect, url_for, render_template, request, flash
import hashlib
import requests
import base64
import shutil
import time
import string
import random
import re
import time
from flask import Response, session
from flask_session import Session
from xml.sax.saxutils import escape

HOST_GENERATOR = os.getenv('HOST_GENERATOR', 'localhost')
HOST_RENDERER = os.getenv('HOST_RENDERER', 'localhost')

def randomString(stringLength=8):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
SESSION_FILE_THRESHOLD = 1000
app.secret_key = randomString(20)
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

# Index page
@app.route('/')
def index():
     if not session.get('id'):
          session["id"] = randomString(20)
     
     return render_template("index.html", content="")

# GET: Shows the user interface to generate reports
# POST: Triggers the report generation in the backend
@app.route('/generate', methods=['GET', 'POST'])
def generate():
     if not session.get('id'):
          session["id"] = randomString(20)
     if request.method == 'POST':
          year_start = request.form["startyear"]
          year_end = request.form["endyear"]
          country = escape(request.form["country"].replace("\"", "").replace("'", ""))

          if int(re.match(r'\d+',year_start)[0]) < 1960 or int(re.match(r'\d+',year_start)[0])  > 2021:
               return render_template("error.html", errormessage="Invalid starting year!")

          if int(re.match(r'\d+',year_end)[0]) < 1960 or int(re.match(r'\d+',year_end)[0]) > 2021:
               return render_template("error.html", errormessage="Invalid ending year!")
          
          report_id = randomString()
          resp = requests.post(f"http://{HOST_GENERATOR}:5001/generate_report", json={"report_id":report_id, "startyear":year_start, "endyear":year_end, "country":country, "session_id":session["id"]})
          if resp.status_code == 200:
               # Report has been generated, request the redirect to the PDF renderer
               resp = requests.get(f"http://{HOST_GENERATOR}:5001/send_report", params={"report_id":report_id, "session_id":session["id"], "target": f"http://{HOST_RENDERER}:5002/render_report"})
               
               # Now we wait for the renderer
               # Dirty fix: Flask runs as HTTP, but is served as HTTPS in the browser
               # Hence we have to perform the redirect via JS
               return Response(f"""<html><body><script>
setTimeout(function () {{
  window.location.href = "/generating?report_id={report_id}&session_id={session["id"]}";
}}, 1000); //will call the function after 2 secs.
</script></body></html>""", 200)

          return render_template("generating.html", report_id=report_id, session_id=session["id"], errormessage="Failed to generate report")
     else:
          return render_template("generate.html", content="")

# Staging page to wait, till the report is generated
# Redirects automatically to /generated
@app.route('/generating', methods=['GET', 'POST'])
def generating():
     report_id = request.args.get("report_id")
     session_id = request.args.get("session_id")

     return render_template("generating.html", report_id=report_id, session_id=session_id)

# Retrieves a generated report by id from the backend
@app.route('/generated', methods=['GET', 'POST'])
def generated():
     session_id = request.args.get("session_id")
     report_id = request.args.get("report_id")

     resp = requests.get(f"http://{HOST_RENDERER}:5002/get_report", params={"report_id":report_id, "session_id":session_id})
     if resp.status_code == 404:
          return render_template("generated.html", report_id=report_id, errormessage="Report not found. Maybe something went wrong")

     return Response(resp.content, "200", mimetype="application/pdf")

if __name__ == "__main__":
    app.run()