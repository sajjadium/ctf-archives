from flask import Flask, request, render_template, Response, make_response

app = Flask(__name__)


@app.route("/")
def homepage() -> Response:
    """The homepage for the app"""
    cookie = request.cookies.get("cookie", "")

    # Render normal page
    response = make_response(render_template("index.html", user=cookie))
    response.set_cookie("cookie", cookie if len(cookie) > 0 else "user")
    return response


if __name__ == "__main__":
    app.run(debug=True)
