from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
from pathlib import Path
from subprocess import PIPE, Popen
import string
import random

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def check_file(filename):
    if Path(filename).is_file():
        return True
    else:
        return False

app = Flask(__name__)
cors = CORS(app)

@app.route('/save',methods = ['POST'])
@cross_origin()
def save():
    c_type=request.form['c_type']
    print('ctype-(>'+c_type)
    if (c_type == 'php'):
        code=request.form['code']
        if (len(code)<100):
            filename=get_random_string(6)+'.php'
            path='/home/app/test/'+filename
            f=open(path,'w')
            f.write(code)
            f.close()
            return filename
        
        else:
            return 'failed'
    """elif (c_type == 'python'):
        code=request.args.get('code')
        if (len(code)<30):
            filename=get_random_string(6)+'.py'
            path='/home/app/testpy/'+filename
            f=open(path,'w')
            f.write(code)
            f.close()
            return filename
        else:
            return 'failed'"""

@app.route('/compile',methods = ['POST'])
@cross_origin()
def compile():
    c_type=request.form['c_type']
    filename=request.form['filename']
    if (c_type == 'php'):
        if (filename[-3:]=='php'):
            if (check_file('/home/app/test/'+filename)):
                path='/home/app/test/'+filename
                cmd='php -c php.ini '+path
                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                return stdout
            else:
                return 'failed'
        else:
            return 'noop'
    elif (c_type == 'python'):
        if (filename[-2:]=='py'):
            if (check_file('/home/app/test/'+filename)):
                cmd='python3 '+filename
                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                return stdout
            else:
                return 'failed'
        else:
            return 'noop'

if __name__ == '__main__':
   app.run()