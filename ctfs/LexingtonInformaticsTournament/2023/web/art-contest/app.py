from flask import Flask, render_template, request, send_from_directory, send_file
import os
import secrets
import time
from playwright.sync_api import sync_playwright
from multiprocessing import Lock

app = Flask(__name__)

FLAG = open("flag.txt").read()

grader_lock = Lock()

def judge_art(id):
    with grader_lock:
        if os.path.isfile("uploads/" + id + "/grader.lock"):
            return
        with open("uploads/" + id + "/grader.lock", "w") as f:
            pass
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        fname = None
        with open("uploads/" + id + "/grader.filename") as f:
            fname = f.read()
        context.new_page().goto("file://" + os.getcwd() + "/uploads/" + id + "/" + fname)
        # TODO: actually grade the art
        # by default, don't assign winners
        os.makedirs("status", exist_ok=True)
        with open("status/" + id, "w") as f:
            f.write("not winner\n")
        time.sleep(0.5)
        context.new_page().goto("http://localhost:5000/status/" + id)
        status_page = context.pages[1]
        if status_page.url == "http://localhost:5000/status/" + id and "winner!!" in status_page.content():
            with open("status/" + id, "w") as f:
                f.write("Congrats! Your submission, " + fname + ", won! Here's the flag: " + FLAG + "\n")
        else:
            with open("status/" + id, "w") as f:
                f.write("Your submission, " + fname + ", did not win. Thank you for taking your time to enter this contest.\n")  
        context.close()
        browser.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    token = secrets.token_hex(32)
    base_dir = os.path.abspath("uploads/" + token)
    abs_path = os.path.abspath(base_dir + "/" + f.filename)
    if base_dir == os.path.commonpath((base_dir, abs_path)):
        ext = os.path.splitext(abs_path)[1]
        if ext == "" or ext == ".txt":
            os.makedirs(os.path.dirname(abs_path))
            f.save(abs_path)
            with open(base_dir + "/grader.filename", "w") as fl:
                fl.write(f.filename)
            return "File uploaded successfully. Thank you for submitting to the 2023 ASCII Art Contest.<br><br>Your submission id is: " + token + " (keep this safe)."
    return "File upload failed! Something went wrong when saving your file. For security purposes, make sure your file does not have an extension or has a .txt extension."

@app.route("/judge", methods=["POST"])
def judge():
    unsanitized_id = request.form["id"]
    sanitized_id = ""
    for ch in unsanitized_id:
        if ch in "0123456789abcdef":
            sanitized_id += ch
    judge_art(sanitized_id)
    return "Thank you. You can view your results <a href=\"/status/" + sanitized_id + "\">here</a>."  

@app.route("/status/<unsanitized_id>")
def status(unsanitized_id):
    sanitized_id = ""
    for ch in unsanitized_id:
        if ch in "0123456789abcdef":
            sanitized_id += ch
    r = None
    with open("status/" + sanitized_id) as f:
        r = f.read()
    return r