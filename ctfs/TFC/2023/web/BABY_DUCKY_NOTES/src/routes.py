from flask import Blueprint, render_template, session, request, jsonify, abort
from database.database import db_login, db_register, db_create_post, db_get_user_posts, db_get_all_users_posts, db_delete_posts, db_delete_all_posts
import re, threading, datetime
from functools import wraps
from bot import bot

USERNAME_REGEX = re.compile('^[A-za-z0-9\.]{2,}$')

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = session.get('username')

        if not username:
            return abort(401, 'Not logged in!')
 
        return f(username, *args, **kwargs)

    return decorator

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/', methods=['GET'])
def index():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', current_date=date)

@web.route('/login')
def login():
    return render_template('login.html')

@web.route('/register')
def register():
    return render_template('register.html')

@web.route('/posts/', methods=['GET'])
@auth_required
def posts(username):
    if username != 'admin':
        return jsonify('You must be admin to see all posts!'), 401

    frontend_posts = []
    posts = db_get_all_users_posts()

    for post in posts:
        try:
            frontend_posts += [{'username': post['username'], 
                                'title': post['title'], 
                                'content': post['content']}]
        except:
            raise Exception(post)

    return render_template('posts.html', posts=frontend_posts)


@web.route('/posts/view/<user>', methods=['GET'])
@auth_required
def posts_view(username, user):
    try:
        posts = db_get_user_posts(user, username == user)
    except:
        raise Exception(username)

    return render_template('posts.html', posts=posts)


@web.route('/posts/create', methods=['GET'])
@auth_required
def posts_create(username):
    return render_template('create.html', username=username)

@api.route('/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify('JSON is needed'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify('Username and password required!'), 401
    
    if type(username) != str or type(password) != str:
        return jsonify('Username or password wrong format!'), 402 
    
    user = db_login(username, password)
    
    if user:
        session['username'] = username
        return jsonify('Success login'), 200
        
    return jsonify('Invalid credentials!'), 403

@api.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return jsonify('JSON is needed'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    
    if not username or not password:
        return jsonify('Username and password required!'), 402
    
    if type(username) != str or type(password) != str:
        return jsonify('Username or password wrong format!'), 402 
    
    if USERNAME_REGEX.match(username) == None:
        return jsonify('Can\'t create an account with that username'), 402

    result = db_register(username, password)
    
    if result:
        return jsonify('Success register'), 200
        
    return jsonify('Account already existing!'), 403

@api.route('/posts', methods=['POST'])
@auth_required
def api_create_post(username): 
    if not request.is_json:
        return jsonify('JSON is needed'), 400
    
    data = request.get_json()
    title = data.get('title', None)
    content = data.get('content', '')
    hidden = data.get('hidden', None)
    
    if not content or hidden == None:
        return jsonify('Content and hidden value required!'), 401
    
    if title and type(title) != str:
         return jsonify('Title value wrong format!'), 402 
    if type(content) != str or type(hidden) != bool:
        return jsonify('Content and hidden value wrong format!'), 402 
    
    db_create_post(username, {"title": title, "content": content, "hidden": hidden})

    return jsonify('Post created successfully!'), 200

@api.route('/report', methods=['POST'])
@auth_required
def api_report(username): 
    thread = threading.Thread(target=bot, args=(username,))
    thread.start()

    return jsonify('Post reported successfully!'), 200

@api.route('/posts', methods=['DELETE'])
@auth_required
def api_delete_posts(username): 
    db_delete_posts(username)

    return jsonify('All posts deleted successfully!'), 200

@api.route('/posts/all', methods=['DELETE'])
@auth_required
def api_delete_all_posts(username): 
    db_delete_all_posts()

    return jsonify('All posts deleted successfully!'), 200