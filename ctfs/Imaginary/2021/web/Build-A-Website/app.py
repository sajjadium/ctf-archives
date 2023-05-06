#!/usr/bin/env python3

from flask import Flask, render_template_string, request, redirect, url_for
from base64 import b64encode, b64decode

app = Flask(__name__)

@app.route('/')
def index():
  # i dont remember how to return a string in flask so
  # here goes nothing :rooNervous:
  return render_template_string(open('templates/index.html').read())

@app.route('/backend')
def backend():
  website_b64 = b64encode(request.args['content'].encode())
  return redirect(url_for('site', content=website_b64))

@app.route('/site')
def site():
  content = b64decode(request.args['content']).decode()
  #prevent xss
  blacklist = ['script', 'iframe', 'cookie', 'document', "las", "bas", "bal", ":roocursion:"] # no roocursion allowed
  for word in blacklist:
    if word in content:
      # this should scare them away
      content = "*** stack smashing detected ***: python3 terminated"
  csp = '''<head>\n<meta http-equiv="Content-Security-Policy" content="default-src 'none'">\n</head>\n'''
  return render_template_string(csp + content)
