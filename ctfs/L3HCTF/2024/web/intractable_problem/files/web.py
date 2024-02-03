import flask
import time
import random
import os
import subprocess

codes=""
with open("oj.py","r") as f:
    codes=f.read()
flag=""
with open("/flag","r") as f:
    flag=f.read()
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('ui.html')

@app.route('/judge', methods=['POST'])
def judge():
    code = flask.request.json['code'].replace("def factorization(n: string) -> tuple[int]:","def factorization(n):")
    correctstr = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 20))
    wrongstr = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 20))
    print(correctstr,wrongstr)
    code=codes.replace("Correct",correctstr).replace("Wrong",wrongstr).replace("<<codehere>>",code)

    filename = "upload/"+str(time.time()) + str(random.randint(0, 1000000))
    with open(filename + '.py', 'w') as f:
        f.write(code)

    try:
        result = subprocess.run(['python3', filename + '.py'], stdout=subprocess.PIPE, timeout=5).stdout.decode("utf-8")
        os.remove(filename + '.py')
        print(result)
        if(result.endswith(correctstr+"!")):
            return flask.jsonify("Correct!flag is "+flag)
        else:
            return flask.jsonify("Wrong!")
    except:
        os.remove(filename + '.py')
        return flask.jsonify("Timeout!")

if __name__ == '__main__':
    app.run("0.0.0.0")