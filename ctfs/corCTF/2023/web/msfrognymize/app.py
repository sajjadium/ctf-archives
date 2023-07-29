import os
import piexif
import tempfile
import uuid

from PIL import Image, ExifTags
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from flask import Flask, request, send_file, render_template
from urllib.parse import unquote
from werkzeug.utils import secure_filename

from celery_config import celery_app
from tasks import process_image

app = Flask(__name__)

celery_app.conf.update(app.config)

UPLOAD_FOLDER = 'uploads/'
ENCRYPTION_KEY = open("/flag.txt", "rb").readline()


def hmac_sha256(data):
    h = hmac.HMAC(ENCRYPTION_KEY, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize().hex()


def encrypt_exif_data(exif_data):
    new_exif_data = {}
    for tag, value in exif_data.items():
        if tag in ExifTags.TAGS:
            tag_name = ExifTags.TAGS[tag]
            if tag_name == "Orientation":
                new_exif_data[tag] = 1
            else:
                new_exif_data[tag] = value
        else:
            new_exif_data[tag] = hmac_sha256(value)
    return new_exif_data


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                img = Image.open(file)
                if img.format != "JPEG":
                    return "Please upload a valid JPEG image.", 400

                exif_data = img._getexif()
                encrypted_exif = None
                if exif_data:
                    encrypted_exif = piexif.dump(encrypt_exif_data(exif_data))
                filename = secure_filename(file.filename)
                temp_path = os.path.join(tempfile.gettempdir(), filename)
                img.save(temp_path)

                unique_id = str(uuid.uuid4())
                new_file_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.png")
                process_image.apply_async(args=[temp_path, new_file_path, encrypted_exif])

                return render_template("processing.html", image_url=f"/anonymized/{unique_id}.png")

            except Exception as e:
                return f"Error: {e}", 400

    return render_template("index.html")


@app.route('/anonymized/<image_file>')
def serve_image(image_file):
    file_path = os.path.join(UPLOAD_FOLDER, unquote(image_file))
    if ".." in file_path or not os.path.exists(file_path):
        return f"Image {file_path} cannot be found.", 404
    return send_file(file_path, mimetype='image/png')


if __name__ == '__main__':
    app.run()
