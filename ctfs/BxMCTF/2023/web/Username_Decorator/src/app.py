from flask import Flask, render_template_string, request
import re

app = Flask(__name__)
app.config['FLAG_LOCATION'] = 'os.getenv("FLAG")'

def validate_username(username):
  return bool(re.fullmatch("[a-zA-Z0-9._\[\]\(\)\-=,]{2,}", username))

@app.route('/', methods=['GET', 'POST'])
def index():
    prefix = ''
    username = ''
    suffix = ''
    
    if request.method == 'POST':
      prefix = (request.form['prefix'] or '')[:2]
      username = request.form['username'] or ''
      suffix = (request.form['suffix'] or '')[:2]
      if not validate_username(username): username = 'Invalid Username'
	
    template = '<!DOCTYPE html><html><body>\
    <form action="" method="post">\
      Prefix: <input name="prefix"> <br>\
      Username: <input name="username"> <br>\
      Suffix: <input name="suffix"> <br> \
      <input type="submit" value="Preview!">\
    </form><h2>%s %s %s</h2></body></html>' % (prefix, username, suffix)
    return render_template_string(template)

@app.route('/flag')
def get_flag():
  return 'Nein'
  import os
  return eval(app.config['FLAG_LOCATION'])