from flask import Flask, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import random
import string
import faker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

fake = faker.Faker()
db = SQLAlchemy(app)

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

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users), 200

@app.route("/auth")
def auth():
    response = make_response(redirect('/'))
    response.set_cookie('auth', request.args.get("auth", ""))
    return response, 200

@app.route("/emails/<int:user_id>")
def view_emails(user_id):
    user = User.query.get_or_404(user_id)

    if not "auth" in request.cookies or request.cookies["auth"] != user.password:
        return "Unauthorized", 404

    keyword = request.args.get("search", "")
    emails = Email.query.filter_by(user_id=user.id).filter(
            (Email.subject.contains(keyword)) | (Email.body.contains(keyword))
        ).all()
    if not emails:
        return render_template("emails.html", user=user, emails=emails), 404
    else:
        return render_template("emails.html", user=user, emails=emails), 200

def initialize():
    users = []
    users.append(User(username="admin", email="admin@supersus.corp", password=open("secret.txt").read().strip()))
    for name in ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan", "lime", "maroon", "rose", "banana", "gray", "tan", "coral"]:
        users.append(User(username=name, email=f"{name}@supersus.corp", password="".join(random.choice(string.ascii_letters) for n in range(20))))

    emails = []
    for _ in range(500):
        emails.append(Email(subject=f"Message from {fake.company()}", body=fake.text(), user=random.choice(users)))
    emails.append(Email(subject=f"Message from ImaginaryCTF", body=open("flag.txt").read(), user=users[0]))
    for _ in range(500):
        emails.append(Email(subject=f"Message from {fake.company()}", body=fake.text(), user=random.choice(users)))

    items = []
    items.extend(users)
    items.extend(emails)

    db.session.add_all(items)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        os.system("rm /database.db")
        db.create_all()
        initialize()
        app.run("0.0.0.0", port=8080)
