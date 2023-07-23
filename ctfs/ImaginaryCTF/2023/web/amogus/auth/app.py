from flask import Flask, request, make_response, redirect, url_for
from jinja2 import Environment, select_autoescape, FileSystemLoader
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
loader = FileSystemLoader(searchpath="templates/")
env = Environment(loader=loader)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    emails = db.relationship("Email", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Email('{self.subject}', '{self.body}')"

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = request.args.get("error", "")
        return make_response(env.get_template("login.html").render(error=error))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(f"http://mail.supersus.corp/auth?auth={password}")
        else:
            error = "Invalid username or password."
            return redirect(url_for("login", error=error))

if __name__ == "__main__":
    with app.app_context():
        app.run("0.0.0.0", port=8081)
