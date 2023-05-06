from flask import *
from waitress import serve
from os import environ

PORT = environ.get("port", 1337)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index(): return render_template("index.html")

@app.route("/blocked.html")
def blocked(): return render_template("blocked.html")

@app.route("/import-history.html")
def import_history(): return render_template("import-history.html")

@app.route("/<path:url>")
def viewer(url): return render_template("viewer.html")

if __name__ == "__main__":
	print(f"Server running on port {PORT}")
	serve(app, host="0.0.0.0", port=PORT)