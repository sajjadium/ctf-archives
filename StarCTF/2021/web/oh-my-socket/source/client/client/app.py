from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    return open(__file__).read()

@app.route("/file", methods=['GET','POST'])
def file():
    file = request.args.get('name')
    content = open(file).read()
    return content


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
