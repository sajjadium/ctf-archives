from flask import Flask, request, jsonify, render_template
import sqlite3 as sl
import random
import string
import os
import re

if os.path.exists("words.db"):
    os.remove("words.db")

app = Flask("wordgame")
db = sl.connect("words.db", check_same_thread=False)
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ??????????????????????????????????????????????????????????????????????????????EEEEEETTTTTAAAAAIIIIIOOOONNNNSSSSRRRR"

with db:
    flagTable = "flag"+''.join(random.choices(string.ascii_uppercase + string.digits, k=13))
    db.execute("CREATE TABLE IF NOT EXISTS words (word TEXT, nr INT)")
    db.execute(f"CREATE TABLE IF NOT EXISTS {flagTable} (flag TEXT)")
    with open("sowpods.txt") as f:
        for line in f:
            word = line.strip()
            if len(word) == 4:
                db.execute(f"INSERT INTO words VALUES ('{word}', {random.randint(0, 1000000)})")
    with open("flag.txt") as f:
        flag = f.read().strip()
        assert re.search("[^A-Za-z0-9_}{]", flag) == None
        db.execute(f"INSERT INTO {flagTable} VALUES ('{flag}')")

def randPtrn():
    return random.choice(chars)+random.choice(chars)+random.choice(chars)+random.choice(chars)

def checkWd(word):
    query = f"SELECT word FROM words WHERE word = '{word}'"
    ls = db.execute(query).fetchall()
    return len(ls) > 0

def getAns(ptrn):
    query = f"SELECT word FROM words WHERE word LIKE '{ptrn.replace('?','_')}' ORDER BY nr DESC"
    res = db.execute(query).fetchall()
    if res:
        return res[0][0]
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", pattern=randPtrn(), message="")

@app.route("/", methods=["POST"])
def ask():
    ptrn = request.form.get("ptrn")
    word = request.form.get("word")
    regex = re.compile(re.sub("[^A-Za-z.]","",ptrn.replace("?", ".")).upper())
    if not regex.match(word.upper()):
        return render_template("index.html", pattern=randPtrn(), message=f"{word.upper()} ISNT {ptrn}")
    if checkWd(word.upper()):
        return render_template("index.html", pattern=randPtrn(), message=f"{word.upper()} DOES WORK")
    rndAns = getAns(ptrn)
    if rndAns == None:
        return render_template("index.html", pattern=randPtrn(), message=f"LMAO ZERO SOLS")
    padW = word.ljust(max(len(word),len(rndAns)))
    padR = rndAns.ljust(max(len(word),len(rndAns)))
    q = [i for i in range(len(padW)) if padW[i] != padR[i]]
    if len(q) == 0:
        return render_template("index.html", pattern=randPtrn(), message=f"HUHH WHAT")
    return render_template("index.html", pattern=randPtrn(), message=f"{word} ISNT WORD. HINT: CHAR {min(q)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
    