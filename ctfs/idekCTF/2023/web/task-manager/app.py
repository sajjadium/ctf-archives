from flask import Flask, render_template, request, redirect
from taskmanager import TaskManager
import os

app = Flask(__name__)

@app.before_first_request
def init():
    if app.env == 'yolo':
        app.add_template_global(eval)

@app.route("/<path:path>")
def render_page(path):
    if not os.path.exists("templates/" + path):
        return "not found", 404
    return render_template(path)

@app.route("/api/manage_tasks", methods=["POST"])
def manage_tasks():
    task, status = request.json.get('task'), request.json.get('status')
    if not task or type(task) != str:
        return {"message": "You must provide a task name as a string!"}, 400
    if len(task) > 150:
        return {"message": "Tasks may not be over 150 characters long!"}, 400
    if status and len(status) > 50:
        return {"message": "Statuses may not be over 50 characters long!"}, 400
    if not status:
        tasks.complete(task)
        return {"message": "Task marked complete!"}, 200
    if type(status) != str:
        return {"message": "Your status must be a string!"}, 400
    if tasks.set(task, status):
        return {"message": "Task updated!"}, 200
    return {"message": "Invalid task name!"}, 400

@app.route("/api/get_tasks", methods=["POST"])
def get_tasks():
    try:
        task = request.json.get('task')
        return tasks.get(task)
    except:
        return tasks.get_all()

@app.route('/')
def index():
    return redirect("/home.html")

tasks = TaskManager()

app.run('0.0.0.0', 1337)
