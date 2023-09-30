import math
import time
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Don't try this at home, kids
try:
    from backend import create_skribl, init_backend
except:
    from .backend import create_skribl, init_backend

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

skribls = {}
stime = math.floor(time.time())

init_backend(skribls)

class SkriblForm(FlaskForm):
    skribl = StringField('Your message: ', validators=[DataRequired(), Length(1, 250)])
    author = StringField("Your name:", validators=[Length(0, 40)])
    submit = SubmitField('Submit')
	

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SkriblForm()
    message = ""
    if form.validate_on_submit():
        message = form.skribl.data
        author = form.author.data

        key = create_skribl(skribls, message, author)
        return redirect(url_for('view', key=key))
    
    return render_template('index.html', form=form, error_msg=request.args.get("error_msg", ''))

@app.route('/view/<key>', methods=['GET'])
def view(key):
    print(f"Viewing with key {key}")
    if key in skribls:
        message, author = skribls[key]
        return render_template("view.html", message=message, author=author, key=key)
    else:
        return redirect(url_for('index', error_msg=f"Skribl not found: {key}"))
    
@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')


@app.context_processor
def inject_stime():
    return dict(stime=math.floor(time.time()) - stime)
