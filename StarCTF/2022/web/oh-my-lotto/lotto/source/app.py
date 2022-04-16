from flask import Flask, make_response
import secrets

app = Flask(__name__)

@app.route("/")
def index():
    lotto = []
    for i in range(1, 20):
        n = str(secrets.randbelow(40))
        lotto.append(n)
    
    r = '\n'.join(lotto)
    response = make_response(r)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = 'attachment; filename=lotto_result.txt'
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
