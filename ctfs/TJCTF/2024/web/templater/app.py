from flask import Flask, request, redirect
import re

app = Flask(__name__)

flag = open('flag.txt').read().strip()

template_keys = {
    'flag': flag,
    'title': 'my website',
    'content': 'Hello, {{name}}!',
    'name': 'player'
}

index_page = open('index.html').read()

@app.route('/')
def index_route():
    return index_page

@app.route('/add', methods=['POST'])
def add_template_key():
    key = request.form['key']
    value = request.form['value']
    template_keys[key] = value
    return redirect('/?msg=Key+added!')

@app.route('/template', methods=['POST'])
def template_route():
    s = request.form['template']
    
    s = template(s)

    if flag in s[0]:
        return 'No flag for you!', 403
    else:
        return s

def template(s):
    while True:
        m = re.match(r'.*({{.+?}}).*', s, re.DOTALL)
        if not m:
            break

        key = m.group(1)[2:-2]

        if key not in template_keys:
            return f'Key {key} not found!', 500

        s = s.replace(m.group(1), str(template_keys[key]))

    return s, 200

if __name__ == '__main__':
    app.run(port=5000)
