from io import BytesIO
from PIL import Image
from flask import Flask, request, render_template
import base64

app = Flask(__name__, template_folder="")
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
FLAG_PATH = "flag.png"
flag_img = Image.open(FLAG_PATH)

def encrypt_img(img: Image) -> Image:
    # Permutation-only encryption algorithm
    pass

def img_to_data_url(img: Image) -> str:
    f = BytesIO()
    img.save(f, format="PNG")
    img_base64 = base64.b64encode(f.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/upload", methods=["POST"])
def upload():
    # Captcha verification
    pass

    if "image" not in request.files:
        return "Image not found", 403
    files = request.files.getlist('image')
    imgs = []
    for file in files:
        try:
            im = Image.open(file.stream)
        except Exception as e:
            return "Invalid image", 403
        if im.format != "PNG":
            return "Invalid image format: Please upload PNG files", 403
        if im.size[0] > 256 or im.size[1] > 256:
            return "Image too large: Maximum allowed size is 256x256", 403
        im = im.convert('L')
        imgs.append(im)

    imgs.append(flag_img)
    try:
        urls = [img_to_data_url(encrypt_img(im)) for im in imgs]
    except Exception as e:
        return "I don't know how but black magic is detected", 403

    return render_template("upload.html", url1=urls[0], url2=urls[1], url3=urls[2])

if __name__ == "__main__":
    app.run(debug=False)
