from flask import Flask, request, render_template, make_response, redirect, send_file
import imghdr
from imghdr import tests
import hashlib
from util import *

# https://stackoverflow.com/questions/36870661/imghdr-python-cant-detec-type-of-some-images-image-extension
# there are no bugs here. just patching imghdr
JPEG_MARK = b'\xff\xd8\xff\xdb\x00C\x00\x08\x06\x06' \
            b'\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'

def test_jpeg1(h, f):
    """JPEG data in JFIF format"""
    if b'JFIF' in h[:23]:
        return 'jpeg'

def test_jpeg2(h, f):
    """JPEG with small header"""
    if len(h) >= 32 and 67 == h[5] and h[:32] == JPEG_MARK:
        return 'jpeg'


def test_jpeg3(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b'JFIF', b'Exif') or h[:2] == b'\xff\xd8':
        return 'jpeg'

tests.append(test_jpeg1)
tests.append(test_jpeg2)
tests.append(test_jpeg3)


def verify_jpeg(file_path):
    try:
        jpeg = Image.open(file_path)
        jpeg.verify()
        if imghdr.what(file_path) != 'jpeg':
            return False
        return True
    except:
        return False


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/')
def index():
    resp = make_response(render_template('upload.html'))
    if not request.cookies.get('session'):
        resp.set_cookie('session', create_token())
    return resp

@app.route('/upload', methods=['POST'])
def upload():
    if not request.cookies.get('session'):
        return redirect('/')
    session = request.cookies.get('session')
    uploaded_file = request.files['file']
    password = request.form['password']
    content = request.form['content']
    upload_name = uploaded_file.filename.replace('../', '') # no traversal!
    output_name = os.path.join('output/', os.path.basename(upload_name))
    image_data = uploaded_file.stream.read()
    image_md5 = hashlib.md5(image_data).hexdigest()
    image_path = f'uploads/{image_md5}.jpeg'
    content_path = f"uploads/{rand_string()}.txt"

    # write temp txt file
    with open(content_path, 'w') as f:
        f.write(content)
        f.close()

    # write temp image file
    with open(image_path, 'wb') as f:
        f.write(image_data)
        f.close()
    
    # verify jpeg validity
    if not verify_jpeg(image_path):
        return 'File is not a valid JPEG!', 400

    # verify session before using it
    session = verify_token(session)
    if not session:
        return 'Session token invalid!', 400
    
    # attempt to embed message in image
    try:
        embed_file(content_path, image_path, output_name, password)
    except:
        return 'Embedding failed!', 400
    
    # append username to output path to prevent vulns
    sanitized_path = f'output/{upload_name}_{session["username"]}'
    try:
        if not os.path.exists(sanitized_path):
            os.rename(output_name, sanitized_path)
    except:
        pass
    try:
        return send_file(sanitized_path)
    except:
        return 'Something went wrong! Check your file name', 400
    


app.run('0.0.0.0', 1337)

