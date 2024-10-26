from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/name/<input_name>', methods=['GET'])
def say_name(input_name):
    if request.method == 'GET':
        if input_name is not None:
            return render_template_string(f"Hello {input_name}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555)