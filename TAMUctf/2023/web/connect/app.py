import flask
import os

def escape_shell_cmd(data):
    for char in data:
        if char in '&#;`|*?~<>^()[]{}$\\':
            return False
        else:
            return True

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/api/curl', methods=['POST'])
def curl():
    url = flask.request.form.get('ip')
    if escape_shell_cmd(url):
        command = "curl -s -D - -o /dev/null " + url + " | grep -oP '^HTTP.+[0-9]{3}'"
        output = os.popen(command).read().strip()
        if 'HTTP' not in output:
            return flask.jsonify({'message': 'Error: No response'})
        return flask.jsonify({'message': output})

    else:
        return flask.jsonify({'message': 'Illegal Characters Detected'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

