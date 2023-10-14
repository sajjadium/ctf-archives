from flask import Flask, render_template, request
import random
import re
import urllib.parse
import sqlite3

app = Flask(__name__)


def waf_cuc_chill(ans):
    # idk, I thought too much of a good thing
    ans = urllib.parse.quote(ans)
    pattern = re.compile(r'(and|0r|substring|subsrt|if|case|cast|like|>|<|(?:/\%2A.*?\%2A/)|\\|~|\+|-|when|then|order|name|url|;|--|into|limit|update|delete|drop|join|version|not|hex|load_extension|round|random|lower|replace|likely|iif|abs|char|unhex|unicode|trim|offset|count|upper|sqlite_version\(\)|#|true|false|max|\^|length|all|values|0x.*?|left|right|mid|%09|%0A|%20|\t)', re.IGNORECASE)
    
    if pattern.search(ans):
        return True
    return False

@app.route("/", methods=["GET"])
def index():
    ran = random.randint(1, 11)
    id, ans= request.args.get("id", default=f"{ran}"), request.args.get("ans", default="")

    if not (id and str(id).isdigit() and int(id) >= 1 and int(id) <= 1301):
        id = 1
    

    db = sqlite3.connect("hehe.db")
    cursor = db.execute(f"SELECT URL FROM QuiBuu WHERE ID = {id}")
    img = cursor.fetchone()[0]

    if waf_cuc_chill(ans):
        return render_template("hack.html")
    
    cursor = db.execute(f"SELECT * FROM QuiBuu where ID = {id} AND Name = '{ans}'")
    result = cursor.fetchall()

    check = 0
    if result != []:
        check = 1
    elif result == [] and ans != "" :
        check = 2

    return render_template("index.html", id=id, img=img, ans=ans, check=check)

if __name__ == "__main__":
    app.run()