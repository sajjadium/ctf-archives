from flask import Flask, Response, request
app = Flask(__name__)

@app.route('/')
def index():
    prefix = bytes.fromhex(request.args.get("p", default="", type=str))
    flag = request.cookies.get("FLAG", default="uiuctf{FAKEFLAG}").encode() #^uiuctf{[0-9A-Za-z]{8}}$ 
    return Response(prefix+flag+b"Enjoy your flag!", mimetype="text/plain")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)
