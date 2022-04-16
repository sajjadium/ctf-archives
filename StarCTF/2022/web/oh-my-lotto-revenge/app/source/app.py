
from flask import Flask,render_template, request
import secrets
import os

app = Flask(__name__, static_url_path='')

def safe_check(s):
    if 'LD' in s or 'HTTP' in s or 'BASH' in s or 'ENV' in s or 'PROXY' in s or 'PS' in s: 
        return False
    return True

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/lotto", methods=['GET', 'POST'])
def lotto():
    message = ''

    if request.method == 'GET':
        return render_template('lotto.html')

    elif request.method == 'POST':
        lotto_key = request.form.get('lotto_key') or ''
        lotto_value = request.form.get('lotto_value') or ''
        try:
            lotto_key = lotto_key.upper()
        except Exception as e:
            print(e)
            message = 'Lotto Error!'
            return render_template('lotto.html', message=message)
        
        if safe_check(lotto_key):
            os.environ[lotto_key] = lotto_value
            try:
                os.system('wget --content-disposition -N lotto')

                if os.path.exists("/app/lotto_result.txt"):
                    lotto_result = open("/app/lotto_result.txt", 'rb').read()
                else:
                    lotto_result = 'result'
                if os.path.exists("/app/guess/forecast.txt"):
                    forecast = open("/app/guess/forecast.txt", 'rb').read()
                else:
                    forecast = 'forecast'

                if forecast == lotto_result:
                    return "You are right!But where is flag?"
                else:
                    message = 'Sorry forecast failed, maybe lucky next time!'
                    return render_template('lotto.html', message=message)
            except Exception as e:
                print("lotto error: ", e)
                message = 'Lotto Error!'
                return render_template('lotto.html', message=message)
                
        else:
            message = 'NO NO NO, JUST LOTTO!'
            return render_template('lotto.html', message=message)
            
@app.route("/forecast", methods=['GET', 'POST'])
def forecast():

    message = ''
    if request.method == 'GET':
        return render_template('forecast.html')
    elif request.method == 'POST':
        if 'file' not in request.files:
            message = 'Where is your forecast?'
            
        file = request.files['file']
        file.save('/app/guess/forecast.txt')
        message = "OK, I get your forecast. Let's Lotto!"
        return render_template('forecast.html', message=message)

@app.route("/result", methods=['GET'])
def result():

    if os.path.exists("/app/lotto_result.txt"):
        lotto_result = open("/app/lotto_result.txt", 'rb').read().decode()
    else:
        lotto_result = ''
    
    return render_template('result.html', message=lotto_result)
        

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080)
