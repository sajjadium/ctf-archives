import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    Blueprint,
    current_app,
    render_template_string,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import subprocess
from dotenv import load_dotenv

load_dotenv()

main = Blueprint("main", __name__)


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads/")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["MAX_CONTENT_LENGTH"] = 128 * 1024  # 128K
    app.register_blueprint(main)
    return app


@main.route("/", methods=["GET", "POST"])
def upload_file():
    messages = None
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))

            # Run OCR on the uploaded image
            process_path = os.path.join("/uploads", file.filename)
            process = subprocess.run(
                f"tesseract \'{process_path}\' \'{process_path}\' -l eng",
                shell=True,
                check=False,
                capture_output=True,
            )
            print(process.args)
            if process.returncode == 0:
                print("Success")
                return redirect(url_for("main.download_file", name=filename + ".txt"))
            else:
                messages = [process.stdout.decode(), process.stderr.decode()]

    return render_template_string(
        """<!doctype html>
<title>OCR As-A-Service</title>
{% if messages %}
<ul class=flashes>
{% for message in messages %}
  <li>{{ message }}</li>
  {% endfor %}
</ul>
{% endif %}
<h1>OCR As-A-Service</h1>
<p>Upload an image and I'll grab the text off it!</p>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
""",
        messages=messages,
    )


@main.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)
