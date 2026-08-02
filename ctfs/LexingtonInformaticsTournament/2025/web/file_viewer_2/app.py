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
    <p>Click on the button below to view a random sample file. Also, you can't look at my secrets anymore -- I secured that directory this time around ;)</p>
    <button onclick="window.location.href='/view-file?file=' + getRandomFile()">View Random File</button>
    <script>
        function getRandomFile() {
            const files = ["sample1.txt", "sample2.txt", "sample3.txt"];
            return files[Math.floor(Math.random() * files.length)];
        }
    </script>
    <p>Oh also -- here are some pictures from my most recent vacation. Take a look at these, since you can't look at my secrets now anyway :)</p>
    <img src="/view-file?file=images/sailboat.jpg" width="200" height="auto">
    <img src="/view-file?file=images/seagulls.jpg" width="200" height="auto">
    <img src="/view-file?file=images/sunset.jpg" width="200" height="auto">
    <img src="/view-file?file=images/beach.jpg" width="200" height="auto">
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/view-file')
def view_file():
    filename = request.args.get('file', '')
    
    if filename[0:2] == '..':
        return abort(400, "Stop trying to look at my secrets >:(")
    
    filepath = os.path.join('files', filename)

    print(filepath)
    
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return abort(404)
    
    return send_file(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

