from flask import Flask, request, send_file, abort, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My File View</title>
</head>
<body>
    <h1>Welcome to my file viewer!</h1>
    <p>Click on the button below to view a random sample file.</p>
    <button onclick="window.location.href='/view-file?file=' + getRandomFile()">View Random File</button>
    <script>
        function getRandomFile() {
            const files = ["sample1.txt", "sample2.txt", "sample3.txt"];
            return files[Math.floor(Math.random() * files.length)];
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/view-file')
def view_file():
    filename = request.args.get('file', '')
    filepath = os.path.join('files', filename)
    
    if not os.path.exists(filepath):
        return abort(404)
    
    return send_file(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
