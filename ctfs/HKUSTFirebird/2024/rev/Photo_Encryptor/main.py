from flask import Flask, render_template, request
import hashlib
from random import *
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', msg='', image_b64='')
    
    image = request.files['file']
    im = Image.open(image)
    pix = im.load()
    width, height = im.size

    if (width > 720) or (height > 405):
        return render_template('index.html', msg='The image is too large!', image_b64='')

    if (im.format != 'PNG'):
        return render_template('index.html', msg='You can only upload an PNG image!', image_b64='')

    key = '<**CENSORED**>'

    seed(hashlib.md5(key.encode()).hexdigest().encode())
    
    for x in range(width):
        for y in range(height):
            pix[x, y] = (pix[x, y][0] ^ pix[(x+randint(0, width))%width, (y+randint(0, height))%height][0],
                        pix[x, y][1] ^ pix[(x+randint(0, width))%width, (y+randint(0, height))%height][1],
                        pix[x, y][2] ^ pix[(x+randint(0, width))%width, (y+randint(0, height))%height][2])
    
    for x in range(width):
        for y in range(height):
            pix[x, y] = (pix[x, y][0] ^ ord(key[(x+y)%len(key)]), 
                        pix[x, y][1] ^ ord(key[(x+y)%len(key)]),
                        pix[x, y][2] ^ ord(key[(x+y)%len(key)]))
    
    imgByteArr = io.BytesIO()
    im.save(imgByteArr, format='png')
    encoded_img_data = base64.b64encode(imgByteArr.getvalue())

    return render_template("index.html", msg='Your image has been encrypted!', image_b64=encoded_img_data.decode('utf-8'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)