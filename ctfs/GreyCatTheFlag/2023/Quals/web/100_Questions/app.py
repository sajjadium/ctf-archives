from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    qn_id, ans= request.args.get("qn_id", default="1"), request.args.get("ans", default="")

    # id check, i don't want anyone to pollute the inputs >:(
    if not (qn_id and qn_id.isdigit() and int(qn_id) >= 1 and int(qn_id) <= 100):
        # invalid!!!!!
        qn_id = 1
    
    # get question
    db = sqlite3.connect("database.db")
    cursor = db.execute(f"SELECT Question FROM QNA WHERE ID = {qn_id}")
    qn = cursor.fetchone()[0]

    # check answer
    cursor = db.execute(f"SELECT * FROM QNA WHERE ID = {qn_id} AND Answer = '{ans}'")
    result = cursor.fetchall()
    correct = True if result != [] else False

    return render_template("index.html", qn_id=qn_id, qn=qn, ans=ans, correct=correct)

if __name__ == "__main__":
    app.run()