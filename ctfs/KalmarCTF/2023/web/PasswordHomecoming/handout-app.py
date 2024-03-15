from flask import Flask, render_template, make_response

app = Flask(__name__)
# ...

@app.before_request
def enable_firewall():
    if firewall.is_banned(...):
        return make_response("Your IP has been reported for abusing this websites functionality. Please behave and wait 60 seconds!")


def do_render_template(filename, host, **context):
    # This is not really the challenge, just showing you this awesome way of translating websites:
    result = render_template(filename, **context)
    if 'dansk' in host:
        result = result.replace("o", "ø").replace("a", "å")
    elif 'l33t' in host:
        result = result.replace("e", "3").replace("l", "1").replace("o", "0")
    elif 'pirate' in host:
        ...
    return result
    

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    ...

@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    ...

@app.route('/register', methods=['GET','POST'])
def register():
    ...

@app.route('/login', methods=['GET','POST'])
def login_form():
    ...

@app.route('/abuse')
def ban_ip():
    ...

@app.route('/logout') 
def logout():
    ...

@app.route("/")
def index():
    ...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, debug=True)
