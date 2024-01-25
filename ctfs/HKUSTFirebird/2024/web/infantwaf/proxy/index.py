from flask import Flask, request, render_template_string
from requests import get
from random import uniform

app = Flask(__name__)
PORT = 80

upstream = 'http://infantwaf.backend'

@app.route('/', methods=['GET'])
def proxy():
    q = request.args.get('giveme')
    if q is not None:
        if q != 'proxy':
            return '🈲'
        elif 'flag' in request.query_string.decode():
            return '🚩'
        else:
            return get(f'{upstream}/?{request.query_string.decode()}').content
    else:
        with open("index.html", "r") as fp:
            out = fp.read()
        return render_template_string(out, text_rot=uniform(-5.0, 5.0), button_rot=uniform(-15.0, 15.0), button_trans=uniform(0.0, 10.0))
        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)