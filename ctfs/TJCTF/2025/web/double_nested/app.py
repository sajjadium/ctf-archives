from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    i=request.args.get("i", "double-nested")
    return render_template("index.html", i=sanitize(i))

def sanitize(input):
    input = re.sub(r"^(.*?=){,3}", "", input)
    forbidden = ["script", "http://", "&", "document", '"']
    if any([i in input.lower() for i in forbidden]) or len([i for i in range(len(input)) if input[i:i+2].lower()=="on"])!=len([i for i in range(len(input)) if input[i:i+8].lower()=="location"]): return 'Forbidden!'
    return input

@app.route('/gen')
def gen():
    query = sanitize(request.args.get("query", ""))
    return query, 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    app.run()
