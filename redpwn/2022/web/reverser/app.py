from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.get('/')
def index():
    result = '''
        <link rel="stylesheet" href="style.css" />
        <div class="container">
            <h1>Text Reverser</h1>
            Reverse any text... now as a web service!
            <form method="POST">
                <input type="text" name="text">
                <input type="submit" value="Reverse">
            </form>
        </div>
    '''
    return render_template_string(result)


@app.post('/')
def reverse():
    result = '''
        <link rel="stylesheet" href="style.css" />
        <div class="container">
            <h1>Text Reverser</h1>
            Reverse any text... now as a web service!
            <form method="POST">
                <input type="text" name="text">
                <input type="submit" value="Reverse">
            </form>
            <p>Output: %s</p>
        </div>
    '''
    output = request.form.get('text', '')[::-1]
    return render_template_string(result % output)

@app.get('/style.css')
def style():
    return '''
        * {
            font-family: 'Helvetica Neue', sans-serif;
            box-sizing: border-box;
        }

        html, body { margin: 0; }

        .container {
            padding: 2rem;
            width: 90%;
            max-width: 900px;
            margin: auto;
        }

        input:not([type="submit"]) {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
        }
    '''
