#!/usr/bin/env python3

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
    return open('templates/index.html').read()

@app.route('/calc')
def calc():
    query = request.args['query']
    request.args = {}
    request.headers = {} # no outside help!
    request.cookies = {}
    if len(query) > 80: # my exploit is 77 chars, but 80 is such a nice even number
        return "Too long!"
    res = render_template_string("{{%s}}"%query)
    out = ''
    for c in res:
        if c in "0123456789-": # negative numbers are cool
            out += c
    return out
