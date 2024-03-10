from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

import random

app = Flask(__name__)
app.secret_key = "secret_key"

seed = random.getrandbits(32)
random.seed(seed)
flag_no = None

def generate_user_ids():
    global flag_no
    random_numbers = []
    for i in range(1000000):
        random_number = random.getrandbits(32)
        random_numbers.append(random_number)
    flag_no = random_numbers[-1]
    print(flag_no)
    st_id = 624
    end_id = 999999
    del random_numbers[st_id:end_id]
    return random_numbers

user_ids = generate_user_ids()
j = 0

@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global j
    id_no = user_ids[j%624]
    j += 1
    if request.method == 'POST':
        number = int(request.form['number'])
        if number == flag_no:
            return redirect('/flagkeeper')
        else:
            return redirect('/wrongnumber')
    return render_template('dashboard.html', number=id_no)

@app.route('/flagkeeper')
def flagkeeper_dashboard():
    return render_template('flag_keeper.html', user_id=flag_no)

@app.route('/wrongnumber')
def wrong_number():
    return render_template('wrong_number.html')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
