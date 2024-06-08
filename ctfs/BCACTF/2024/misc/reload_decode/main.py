from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index(): #Gets the main page
    return render_template('index.html')

@app.route('/flag')
def getFlag():
    #Get flag from flag.txt
    with open("flag.txt") as f:
        flag = bytearray(f.read().encode())
    flag_str = ""
    for b in flag:
        b = b << 4 ^ ((b << 4 & 0xff) >> 4)
        bm = 1 << random.randint(0, 11)
        cb = b ^ bm
        flag_str += bin(cb)[2:].zfill(12)
        
    return render_template('index.html', joined_flag = flag_str)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
