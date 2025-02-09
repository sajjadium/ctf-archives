from flask import Flask, request, jsonify, abort, render_template_string, session, redirect
import builtins as _b
import sys
import os


app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "default_app_secret")
env = app.jinja_env


KEY = os.getenv("APP_SECRET_KEY", "default_secret_key")



class validator:
    def security():
        return _b
    def security1(a, b, c, d):
        if 'validator' in a or 'validator' in b or 'validator' in c or 'validator' in d:
            return False
        elif 'os' in a or 'os' in b or 'os' in c or 'os' in d:
            return False
        else:
            return True
    
    def security2(a, b, c, d):
        if len(a) <= 50 and len(b) <= 50 and len(c) <= 50 and len(d) <= 50:
            return True
        else :
            return False
        


@app.route("/", methods=["GET", "POST"])
def personalized_card():
    if request.method == "GET":
        return """
        <link rel="stylesheet" href="static/style.css">
        <link href="https://fonts.googleapis.com/css?family=Poppins:300,400,600&display=swap" rel="stylesheet">
        <div class="container">
            <div class="card-generator">
                <h1>Personalized Card Generator</h1>
                <form action="/" method="POST">
                    <label for="sender">Sender's Name:</label>
                    <input type="text" id="sender" name="sender" placeholder="Your name" required maxlength="50">
                    <label for="recipient">Recipient's Name:</label>
                    <input type="text" id="recipient" name="recipient" placeholder="Recipient's name" required maxlength="50">
                    <label for="message">Message:</label>
                    <input type="text" id="message" name="message" placeholder="Your message" required maxlength="50">
                    <label for="message_final">Final Message:</label>
                    <input type="text" id="message_final" name="message_final" placeholder="Final words" required maxlength="50">
                    <button type="submit">Generate Card</button>
                </form>
            </div>
        </div>
        """

    elif request.method == "POST":
        try:
            recipient = request.form.get("recipient", "")
            sender = request.form.get("sender", "")
            message = request.form.get("message", "")
            final_message = request.form.get("message_final", "")
            if validator.security1(recipient, sender, message, final_message) and validator.security2(recipient, sender, message, final_message):
                template = f"""
                    <link rel="stylesheet" href="static/style.css">
                    <link href="https://fonts.googleapis.com/css?family=Poppins:300,400,600&display=swap" rel="stylesheet">
                    <div class="container">
                        <div class="card-preview">
                            <h1>Your Personalized Card</h1>
                            <div class="card">
                                <h2>From: {sender}</h2>
                                <h2>To: {recipient}</h2>
                                <p>{message}</p>
                                <h1>{final_message}</h1>
                            </div>
                            <a class="new-card-link" href="/">Create Another Card</a>
                        </div>
                    </div>
                """
            else :
                template="either the recipient or sender or message input is more than 50 letters"

            app.jinja_env = env    
            app.jinja_env.globals.update({
                'validator': validator()
            })
            return render_template_string(template)

        except Exception as e:
            return f"""
            <link rel="stylesheet" href="static/style.css">
            <div>
                <h1>Error: {str(e)}</h1>
                <br>
                <p>Please try again. <a href="/">Back to Card Generator</a></p>
            </div>
            """, 400
        



@app.route("/debug/test", methods=["POST"])
def test_debug():
    user = session.get("user")
    host = request.headers.get("Host", "")
    if host != "localhost:3030":
        return "Access restricted to localhost:3030, this endpoint is only development purposes", 403
    if not user:
        return "You must be logged in to test debugging.", 403
    try:
        raise ValueError(f"Debugging error: SECRET_KEY={KEY}")
    except Exception as e:
        return "Debugging error occurred.", 500



@app.route("/admin/report")
def admin_report():
    auth_cookie = request.cookies.get("session")
    if not auth_cookie:
        abort(403, "Unauthorized access.")
    try:
        token, signature = auth_cookie.rsplit(".", 1)
        from app.sign import initFn
        signer = initFn(KEY)
        sign_token_function = signer.get_signer()
        valid_signature = sign_token_function(token)

        if valid_signature != signature:
            abort(403, f"Invalid token.")

        if token == "admin":
            return "Flag: p_ctf{Redacted}"
        else:
            return "Access denied: admin only."
    except Exception as e:
        abort(403, f"Invalid token format: {e}")

@app.after_request
def clear_imports(response):
    if 'app.sign' in sys.modules:
        del sys.modules['app.sign']
    if 'app.sign' in globals():
        del globals()['app.sign']
    return response

