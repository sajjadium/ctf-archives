from flask import Flask, request
import requests
app = Flask(__name__)


@app.route('/checkers', methods=["POST"])
def checkers():
    if request.form.get('even'):
        r = requests.get(f'http://checkers:3000/is_even?n={request.form.get("value")}')
    elif request.form.get('odd'):
        r = requests.get(f'http://checkers:3000/is_odd?n={request.form.get("value")}')
    elif request.form.get('number'):
        r = requests.get(f'http://checkers:3000/is_number?n={request.form.get("value")}')
    result = r.json()
    res = result.get('result')
    if not res:
        return str(result.get('error'))
    return str(res)


@app.route('/arithmetic', methods=["POST"])
def arithmetic():
    if request.form.get('add'):
        r = requests.get(f'http://arithmetic:3000/add?n1={request.form.get("n1")}&n2={request.form.get("n2")}')
    elif request.form.get('sub'):
        r = requests.get(f'http://arithmetic:3000/sub?n1={request.form.get("n1")}&n2={request.form.get("n2")}')
    elif request.form.get('div'):
        r = requests.get(f'http://arithmetic:3000/div?n1={request.form.get("n1")}&n2={request.form.get("n2")}')
    elif request.form.get('mul'):
        r = requests.get(f'http://arithmetic:3000/mul?n1={request.form.get("n1")}&n2={request.form.get("n2")}')
    result = r.json()
    res = result.get('result')
    if not res:
        return str(result.get('error'))
    try:
        res_type = type(eval(res))
        if res_type is int or res_type is float:
            return str(res)
        else:
            return "Result is not a number"
    except NameError:
        return "Result is invalid"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
