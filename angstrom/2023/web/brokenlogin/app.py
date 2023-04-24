from flask import Flask, make_response, request, escape, render_template_string

app = Flask(__name__)

fails = 0

indexPage = """
<html>
    <head>
        <title>Broken Login</title>
    </head>
    <body>
        <p style="color: red; fontSize: '28px';">%s</p>
        <p>Number of failed logins: {{ fails }}</p>
        <form action="/" method="POST">
            <label for="username">Username: </label>
            <input id="username" type="text" name="username" /><br /><br />

            <label for="password">Password: </label>
            <input id="password" type="password" name="password" /><br /><br />

            <input type="submit" />
        </form>
    </body>
</html>
"""

@app.get("/")
def index():
    global fails
    custom_message = ""

    if "message" in request.args:
        if len(request.args["message"]) >= 25:
            return render_template_string(indexPage, fails=fails)
        
        custom_message = escape(request.args["message"])
    
    return render_template_string(indexPage % custom_message, fails=fails)


@app.post("/")
def login():
    global fails
    fails += 1
    return make_response("wrong username or password", 401)


if __name__ == "__main__":
    app.run("0.0.0.0")