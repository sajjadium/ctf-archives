from flask import Flask, render_template, request
import sys

app = Flask(__name__)

def factorial(n):
    if n == 0:
        return 1
    else:
        try:
            return n * factorial(n - 1)
        except RecursionError:
            return 1

def filter_path(path):
    # print(path)
    path = path.replace("../", "")
    try:
        return filter_path(path)
    except RecursionError:
        # remove root / from path if it exists
        if path[0] == "/":
            path = path[1:]
        print(path)
        return path

@app.route('/')
def index():
    safe_theme = filter_path(request.args.get("theme", "themes/theme1.css"))
    f = open(safe_theme, "r")
    theme = f.read()
    f.close()
    return render_template('index.html', css=theme)

@app.route('/', methods=['POST'])
def calculate_factorial():
    safe_theme = filter_path(request.args.get("theme", "themes/theme1.css"))

    f = open(safe_theme, "r")
    theme = f.read()
    f.close()
    try:
        num = int(request.form['number'])
        if num < 0:
            error = "Invalid input: Please enter a non-negative integer."
            return render_template('index.html', error=error, css=theme)
        result = factorial(num)
        return render_template('index.html', result=result, css=theme)
    except ValueError:
        error = "Invalid input: Please enter a non-negative integer."
        return render_template('index.html', error=error, css=theme)

if __name__ == '__main__':
    sys.setrecursionlimit(100)
    app.run(host='0.0.0.0')