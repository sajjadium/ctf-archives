import flask
import os

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/img')
def serve_image():
    filename = flask.request.args.get("f", "").replace("../", "")
    path = f'images/{filename}'
    if not os.path.isfile(path):
        return flask.abort(404)
    return flask.send_file(path)

if __name__ == '__main__':
    app.run()
