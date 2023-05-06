from flask import Flask, request, render_template
import os
import advocate
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        url = request.form['url']

        # Prevent SSRF
        try:
            advocate.get(url)

        except:
            return render_template('index.html', error=f"The URL you entered is dangerous and not allowed.")

        r = requests.get(url)
        return render_template('index.html', result=r.text)

    return render_template('index.html')


@app.route('/flag')
def flag():
    if request.remote_addr == '127.0.0.1':
        return render_template('flag.html', FLAG=os.environ.get("FLAG"))

    else:
        return render_template('forbidden.html'), 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True)
