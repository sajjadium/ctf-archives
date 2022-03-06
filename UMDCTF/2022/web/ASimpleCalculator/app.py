from flask import Flask, send_from_directory, request, render_template, json
from secrets import flag_enc, ws

app = Flask(__name__, static_url_path='')


def z(f: str):
    for w in ws:
        if w in f:
            raise Exception("nope")
    return True


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)


@app.route('/calc', methods=['POST'])
def calc():
    val = 0
    try:
        z(request.json['f'])
        val = f"{int(eval(request.json['f']))}"
    except Exception as e:
        val = 0

    response = app.response_class(
        response=json.dumps({'result': val}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
