from flask import Flask, render_template, request, redirect, url_for
import subprocess
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    url_pattern = re.compile(r'^(https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=]+)$')
    url = request.form.get('url')

    if url is None:
        return "No URL provided.", 400

    if not url_pattern.match(url):
        return "Invalid URL format.", 400

    if url:
        command = ['./nuclei', '--silent', '-u', url, '-t', 'custom-templates.yaml']
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if 'info' in result.stdout and '/api/v2/echo' in result.stdout and 'custom-templates' in result.stdout:
                return "TCP1P{fake_flag}"
            else:
                return "Your website isn't vulnerable"
        except subprocess.CalledProcessError:
            return "Error occurred while running command"
    return "Invalid request"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
