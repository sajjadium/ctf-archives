from flask import Flask, Response, render_template_string, request

app = Flask(__name__)


@app.get("/")
def index() -> Response:
    """
    The base service for admin site
    """
    user = request.cookies.get("user", "user")

    # Currently Work in Progress
    return render_template_string(
        f"Sorry {user}, the admin page is currently not open."
    )
