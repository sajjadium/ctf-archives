from flask import Flask, render_template, redirect, request
from uuid import uuid4

app = Flask(__name__)

images = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def post_image():
    img, name = request.json['img'], request.json['name']
    id = uuid4()
    images[id] = {
        'img': img,
        'name': name
    }
    return redirect('/img/' + str(id))


@app.route('/img/<uuid:id>')
def image_id(id):
    if id not in images:
        return redirect('/')

    img = images[id]['img']
    name = images[id]['name']
    return render_template('index.html', px=img, name=name, saved=True)


if __name__ == '__main__':
    app.run(debug=True)
