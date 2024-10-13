from flask import *
import requests

app = Flask(__name__)

@app.errorhandler(requests.exceptions.MissingSchema)
@app.errorhandler(requests.exceptions.InvalidSchema)
def bad_schema(e):
    return 'no HTTP/S?', 400

@app.errorhandler(requests.exceptions.ConnectionError)
def no_connect(e):
    print("CONNECT ERR")
    return 'I did not understand that URL', 400


    
@app.route("/cdn/<path:url>")
def cdn(url):
    mimes = ["image/png", "image/jpeg", "image/gif", "image/webp"]
    r = requests.get(url, stream=True)
    if r.headers["Content-Type"] not in mimes:
        print("BAD MIME")
        return "????", 400
    img_resp = make_response(r.raw.read(), 200)
    for header in r.headers:
        if header == "Date" or header == "Server":
            continue
        img_resp.headers[header] = r.headers[header]
    return img_resp


if __name__ == "__main__":
    app.run(debug=False, port=8081)
