from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import re
import os
import sys
from utils import is_safe_url
from os import urandom, getenv
import requests


## Constants ##

URL_REGEX = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
BASE_URL = f"http://localhost:5000"

## Init Application ##
app = Flask(__name__)
app.secret_key = urandom(512).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

### These are secure :D, Please do not waste time brute forcing ###
FLAG = getenv('FLAG', 'grey{this_is_a_fake_flag}') #Also the password
ADMIN_COOKIE = getenv('ADMIN_COOKIE', 'this_is_fake_cookie')
#######################################################################


#### Models ####
class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content[:20]}...')"
    
class Url(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    
def is_admin() -> bool:
    """Check if the user is an admin"""
    return request.cookies.get('cookie') == ADMIN_COOKIE
    
#### Before First Request ####
if os.path.exists('database.db'):
    os.remove('database.db')
with app.app_context():
    db.create_all()

#### Routes ####
@app.route('/')
def index() -> Response:
    if not is_admin():
        flash('You are not an admin. Please login to continue', 'danger')
        return redirect(f'/login?next={request.path}')

    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if password != FLAG or username != 'admin':
        flash('Wrong password', 'danger')
        return redirect(url_for('index'))

    # If user is admin, set cookie
    next = request.args.get('next', '/')
    response = redirect('/')
    if is_safe_url(next):
        response = redirect(next)

    response.set_cookie('cookie', ADMIN_COOKIE)
    return response

@app.route('/post', methods=['POST'])
def post() -> Response:
    if not is_admin():
        flash('You are not an admin. Please login to continue', 'danger')
        return redirect(f'/login?next={request.path}')


    title = request.form['title']
    content = request.form['content']

    sanitized_content = sanitize_content(content)

    if title and content:
        post = Post(title=title, content=sanitized_content)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('index'))

    flash('Please fill all fields', 'danger')
    return redirect(url_for('index'))

@app.route('/url/<int:id>')
def url(id: int) -> Response:
    """Redirect to the url in post if its sanitized"""
    url = Url.query.get_or_404(id)
    return redirect(url.url)

def sanitize_content(content: str) -> str:
    """Sanitize the content of the post"""

    # Replace URLs with in house url tracker
    urls = re.findall(URL_REGEX, content)
    for url in urls:
        url = url[0]
        url_obj = Url(url=url)
        db.session.add(url_obj)
        content = content.replace(url, f"/url/{url_obj.id}")
    return content


@app.route('/send_post', methods=['GET', 'POST'])
def send_post() -> Response:
    """Send a post to the admin"""
    if request.method == 'GET':
        return render_template('send_post.html')

    url = request.form.get('url', '/')
    title = request.form.get('title', None)
    content = request.form.get('content', None)

    if None in (url, title, content):
        flash('Please fill all fields', 'danger')
        return redirect(url_for('send_post'))
    
    # Bot visit
    url_value = make_post(url, title, content)
    flash('Post sent successfully', 'success')
    flash('Url id: ' + str(url_value), 'info')
    return redirect('/send_post')


def make_post(url: str, title: str, user_content: str) -> int:
    """Make a post to the admin"""
    with requests.Session() as s:
        visit_url = f"{BASE_URL}/login?next={url}"
        resp = s.get(visit_url, timeout=10)
        content = resp.content.decode('utf-8')
        
        # Login routine (If website is buggy we run it again.)
        for _ in range(2):
            print('Logging in... at:', resp.url, file=sys.stderr)
            if "bot_login" in content:
                # Login routine
                resp = s.post(resp.url, data={
                    'username': 'admin',
                    'password': FLAG,
                })

        # Make post
        resp = s.post(f"{resp.url}/post", data={
            'title': title,
            'content': user_content,
        })

        return db.session.query(Url).count()
        
        
if __name__ == '__main__':
    app.run()