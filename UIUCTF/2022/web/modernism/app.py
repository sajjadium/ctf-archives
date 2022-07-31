from flask import Flask, Response, request
app = Flask(__name__)

@app.route('/')
def index():
    prefix = bytes.fromhex(request.args.get("p", default="", type=str))
    flag = request.cookies.get("FLAG", default="uiuctf{FAKEFLAG}").encode() #^uiuctf{[A-Za-z]+}$ 
    return Response(prefix+flag, mimetype="text/plain")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)
