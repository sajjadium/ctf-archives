from flask import Flask, Response

app = Flask(__name__)

flag = open("flag.txt", "r").read()

@app.route("/flag", methods=["GET"])
def index():
    return Response(flag, mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=1337)
