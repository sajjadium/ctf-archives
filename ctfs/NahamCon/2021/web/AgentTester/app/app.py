from flask_uwsgi_websocket import GeventWebSocket
import re
import subprocess

from backend.backend import *

ws = GeventWebSocket(app)


@app.route("/", methods=["GET"])
@login_required
def home():
    success = request.args.get("success", None)
    error = request.args.get("error", None)

    return render_template(
        "templates/index.html",
        user=g.user,
        success=success,
        error=error,
    )


@app.route("/debug", methods=["POST"])
def debug():
    sessionID = session.get("id", None)
    if sessionID == 1:
        code = request.form.get("code", "<h1>Safe Debug</h1>")
        return render_template_string(code)
    else:
        return "Not allowed."


@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):

    if g.user.id == user_id:
        user_now = User.query.get(user_id)
        if request.method == "POST":
            about = request.form.get("about", None)
            email = request.form.get("email", None)

            if email:
                user_now.email = email
            if about:
                user_now.about = about
            if email or about:
                db.session.commit()

    else:
        return redirect(
            url_for("home", error="You are not authorized to access this resource.")
        )

    return render_template(
        "templates/profile.html",
        user=user_now,
    )


@ws.route("/req")
def req(ws):
    with app.request_context(ws.environ):
        sessionID = session.get("id", None)
        if not sessionID:
            ws.send("You are not authorized to access this resource.")
            return

        uAgent = ws.receive().decode()
        if not uAgent:
            ws.send("There was an error in your message.")
            return

        try:
            query = db.session.execute(
                "SELECT userAgent, url FROM uAgents WHERE userAgent = '%s'" % uAgent
            ).fetchone()

            uAgent = query["userAgent"]
            url = query["url"]
        except Exception as e:
            ws.send(str(e))
            return

        if not uAgent or not url:
            ws.send("Query error.")
            return

        subprocess.Popen(["node", "browser/browser.js", url, uAgent])

        ws.send("Testing User-Agent: " + uAgent + " in url: " + url)
        return
