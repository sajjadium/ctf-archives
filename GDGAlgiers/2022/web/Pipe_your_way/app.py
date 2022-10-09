from pickle import FALSE
from flask import Flask, request,render_template
from jinja2 import Template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('./index.html')

@app.route( '/follow_the_light', methods=['GET'])
def F0LL0WM3():
    the_light = request.args.get("input", None)
    if the_light is None:
        return "It's just a white screen keep trying....."
    else:
        for _ in the_light:
            if any(x in the_light for x in {'.','_','|join', '[', ']', 'mro', 'base','import','builtins','attr','request','application','getitem','render_template'}):
                return "NOICE TRY"
            else:
                return Template("Your input: " + the_light).render()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
