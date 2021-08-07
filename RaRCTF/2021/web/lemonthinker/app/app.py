from flask import Flask, request, redirect, url_for
import os
import random
import string
import time # lemonthink

clean = time.time()
app = Flask(__name__)
chars = list(string.ascii_letters + string.digits)

@app.route('/')
def main():
    return open("index.html").read()

@app.route('/generate', methods=['POST'])
def upload():
    global clean
    if time.time() - clean > 60:
      os.system("rm static/images/*")
      clean = time.time()
    text = request.form.getlist('text')[0]
    text = text.replace("\"", "")
    filename = "".join(random.choices(chars,k=8)) + ".png"
    os.system(f"python3 generate.py {filename} \"{text}\"")
    return redirect(url_for('static', filename='images/' + filename), code=301)
  
if __name__ == "__main__":
  app.run("0.0.0.0",1002)
