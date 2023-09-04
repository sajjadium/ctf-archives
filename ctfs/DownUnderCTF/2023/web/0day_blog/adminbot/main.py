from flask import Flask, render_template, request
import urllib.parse as urlparse
import adminbot
import threading

app = Flask(__name__, static_folder='static/', static_url_path='/')
threading.Thread(target=adminbot.worker, daemon=True).start()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/sendadminbot", methods=["POST"])
def send_admin_bot():
    url = request.form.get('url', None)
    if url is None:
        return render_template("index.html", error="No URL was sent!")
    
    url_parsed = urlparse.urlparse(url)
    if not url_parsed.scheme in ['http', 'https']:
        return render_template("index.html", error="Lol trying to be sneaky with different protocols!")
    
    adminbot.admin_queue.put((url,))
    return render_template("index.html", msg="The admin has been sent to your site! Hope you aren't trying to hack them!")

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)