from flask import Flask, request, render_template_string, redirect
import os
import urllib.parse

app = Flask(__name__)

base_directory = "message/"
default_file = "message.txt"

def ignore_it(file_param):
    yoooo = file_param.replace('.', '').replace('/', '')
    if yoooo != file_param:
        return "Illegal characters detected in file parameter!"
    return yoooo

def another_useless_function(file_param):
    return urllib.parse.unquote(file_param)

def url_encode_path(file_param):
    return urllib.parse.quote(file_param, safe='')

def useless (file_param):
    file_param1 = ignore_it(file_param)
    file_param2 = another_useless_function(file_param1)
    file_param3 = ignore_it(file_param2)
    file_param4 = another_useless_function(file_param3)
    file_param5 = another_useless_function(file_param4)
    return file_param5


@app.route('/')
def index():
    return redirect('/read_secret_message?file=message')

@app.route('/read_secret_message')
def read_file(file_param=None):
    file_param = request.args.get('file')
    file_param = useless(file_param)
    print(file_param)
    file_path = os.path.join(base_directory, file_param)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return 'File not found! or maybe illegal characters detected'
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4053)
