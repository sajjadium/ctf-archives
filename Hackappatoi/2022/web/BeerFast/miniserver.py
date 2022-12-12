from flask import Flask
import secrets
import sys
import os


app = Flask(__name__)


@app.route('/')
def index():
    raise Exception('test')


if __name__ == '__main__':
    # generate stronger pin
    if "WERKZEUG_DEBUG_PIN" not in os.environ:
        rand_pin = 100000000000000 + secrets.randbelow(999999999999999)
        rand_pin = "-".join([str(rand_pin)[i:i + 3] for i in range(0, len(str(rand_pin)), 3)])
        os.environ["WERKZEUG_DEBUG_PIN"] = rand_pin
    app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
