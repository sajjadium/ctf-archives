from flask import Flask, session, redirect, request, flash, send_file, url_for, render_template, send_from_directory
import os


app = Flask(__name__)
app.secret_key = os.urandom(32)

SESS_BASE_DIR = "/tmp/uploads"

if not os.path.isdir(SESS_BASE_DIR):
    os.mkdir(SESS_BASE_DIR)

# We only allow files for serious business use-cases
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_file(filename):
    return filename.replace("..", "_")


def create_session(sess_id):
    sess_dir = os.path.join(SESS_BASE_DIR, sess_id)

    if not os.path.isdir(sess_dir):
        os.mkdir(sess_dir)


def list_files(sess_id):
    sess_dir = os.path.join(SESS_BASE_DIR, sess_id)
    return os.listdir(sess_dir)


@app.route('/')
def index():
    if "ID" not in session:
        sess_id = os.urandom(32).hex()
        session["ID"] = sess_id
        create_session(sess_id)

    files = []
    for file in list_files(session["ID"]):
        files.append(
            {
                "name": file,
                "url": "/dl/" + session["ID"] + "/" + file
            }
        )

    return render_template("index.html", files=files)


@app.route("/upload.html")
def upload_html():
    if "ID" not in session:
        return redirect("/")
    return render_template("upload.html")


@app.route("/dl/<string:sess_id>/<string:file_name>")
def dl(sess_id, file_name):
    path = os.path.join(
        SESS_BASE_DIR,
        normalize_file(sess_id),
        normalize_file(file_name)
    )
    if os.path.exists(path):
        return send_file(path)
    else:
        flash("File does not exist.")
        return redirect(url_for(index))


@app.route('/download_all')
def download_all():
    if "ID" not in session:
        return redirect("/")

    sess_id = session["ID"]
    sess_dir = os.path.join(SESS_BASE_DIR, sess_id)

    res = os.system(f"cd {sess_dir} && tar czf /tmp/{sess_id}.tgz *")
    if res != 0:
        flash("Something went wrong.")
        return redirect("/")
    return send_file(f"/tmp/{sess_id}.tgz", attachment_filename=f"{sess_id}.tgz")


@app.route('/upload', methods=["POST"])
def upload():
    if "ID" not in session:
        return redirect("/")

    if 'file' not in request.files:
        flash('No file part')
        return redirect("/")
    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        f_content = file.stream.read()
        if len(f_content) > 1024:
            flash("Your file is too big! Buy premium to upload bigger files!")
            return redirect('/')
        filename = normalize_file(file.filename)
        with open(os.path.join(SESS_BASE_DIR, session["ID"], filename), "wb") as f:
            f.write(f_content)
        return redirect("/")
    else:
        flash("Invalid file type submitted!")
        return redirect('/')

    return redirect("/")


@app.route('/static/<path:p>')
def staticfiles(p):
    return send_from_directory("static", p)


if __name__ == '__main__':
    app.run()
