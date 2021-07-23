import os
import hashlib
import tempfile
from exiftool import ExifTool
from flask import Flask, request, jsonify

app = Flask(__name__, template_folder="views", static_folder="public", static_url_path="/")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024
secret = os.getenv("SECRET") or "BSidesTLV2021{This_Is_Not_The_Flag}"
if len(secret) < 35:
    raise Exception("Secret size should be 35 or above")


def parse_metadata(metadata, filter_keys=None):
    filter_keys = filter_keys or []
    parsed_metadata = {}
    for key, value in metadata.items():
        keys = key.split(":")

        o = parsed_metadata
        kl = len(keys)
        for i, k in enumerate(keys):
            if k not in o:
                o[k] = {}

            if i < kl - 1:
                o = o[k]
                continue

            o[k] = value

    for k in filter_keys:
        parsed_metadata.pop(k)

    return dict(parsed_metadata)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/view", methods=["POST"])
def view():
    token = request.form.get("token")
    if not token:
        return jsonify({"error": "empty token"})

    images = request.files.getlist("image[]")
    if not images:
        return jsonify({"error": "empty image"})

    image_streams = []
    mac = hashlib.sha1(secret.encode())
    for image in images:
        if not image.mimetype.startswith("image/"):
            return jsonify({"error": "bad image"})

        image_stream = image.stream.read()
        mac.update(image_stream)
        image_streams.append(image_stream)

    if token != mac.hexdigest():
        return jsonify({"error": "bad token"})

    metadata = []
    try:
        with ExifTool() as et:
            for i, image_stream in enumerate(image_streams):
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(image_stream)
                    tmp.flush()
                    tmp.close()

                    parsed_metadata = {
                        "SourceFile": images[i].filename,
                        **parse_metadata(et.get_metadata(tmp.name), filter_keys=["File", "SourceFile"])
                    }
                    metadata.append(parsed_metadata)

                try:
                    os.unlink(tmp.name)
                except Exception as ex:
                    pass

    except Exception as ex:
        return jsonify({"error": str(ex)})

    return jsonify(metadata[0] if len(metadata) < 2 else metadata)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
