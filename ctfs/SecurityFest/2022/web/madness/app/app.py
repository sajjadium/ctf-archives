# coding=utf-8
from flask import Flask, jsonify, make_response, render_template, request, redirect
import dns.resolver
from werkzeug.urls import url_fix

import re
app = Flask(__name__, static_url_path="/app/static")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    if path == "":
        return redirect("/app", code=301)
    return render_template('index.html', prefix="/"+request.path.lstrip("/"))

@app.route('/app/api/lookup/<string:domain>')
def lookup(domain):
    if re.match(r"^[a-z.-]+$", domain):
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['1.1.1.1']
        out = []
        try:
            for item in my_resolver.query(domain, 'A'):
                out.append(str(item))
            return make_response(jsonify({"status":"OK", "result":out}))
        except Exception as e:
            return make_response(jsonify({"status":"ERROR", "result":str(e)}))
    else:
        e = "invalid domain (^[a-z.-]+) {}".format(domain)
        return make_response(jsonify({"status":"ERROR", "result":str(e)}))

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self' cloudflare-dns.com; img-src *"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)