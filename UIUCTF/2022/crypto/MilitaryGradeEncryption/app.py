from flask import Flask, render_template, request
from cipher import custom_encrypt

app = Flask(__name__)

@app.route("/", methods = ["get"])
def home_page():
    return render_template("home.html")

@app.route("/encrypt", methods = ["get", "post"])
def encrypt():
    if request.method == "POST":
        user_data = dict(request.form)
        try:
            ciphertext = custom_encrypt(user_data["data"].encode(), user_data["pin"].zfill(6).encode(), int(user_data["key_size"]))
            return render_template("encrypt.html", not_entered_data = False, data = ciphertext)
        except:
            return render_template("encrypt.html", not_entered_data = True, error = True)
    return render_template("encrypt.html", not_entered_data = True, error = False)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1337)
