from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    code = request.args.get("code")
    if not code:
        return render_template("index.html")

    try:
        exec(code)
    except:
        pass

    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31416)
