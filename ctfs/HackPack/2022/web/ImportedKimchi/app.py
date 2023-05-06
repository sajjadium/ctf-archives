import uuid
from flask import *
from flask_bootstrap import Bootstrap
import pickle
import os

app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'sup3r s3cr3t k3y'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

images = set()
images.add('bibimbap.jpg')
images.add('galbi.jpg')
images.add('pickled_kimchi.jpg')

@app.route('/')
def index():
    return render_template("index.html", images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.files["image"]
        if image and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            # special file names are fun!
            extension = "." + image.filename.split(".")[-1].lower()
            fancy_name = str(uuid.uuid4()) + extension

            image.save(os.path.join('./images', fancy_name))
            flash("Successfully uploaded image! View it at /images/" + fancy_name, "success")
            return redirect(url_for('upload'))

        else:
            flash("An error occured while uploading the image! Support filetypes are: png, jpg, jpeg", "danger")
            return redirect(url_for('upload'))

    else:
        return render_template("upload.html")

@app.route('/images/<filename>')
def display_image(filename):
    try:
        pickle.loads(open('./images/' + filename, 'rb').read())
    except:
        pass
    return send_from_directory('./images', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
