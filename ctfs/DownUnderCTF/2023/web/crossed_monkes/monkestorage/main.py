from flask import Flask, request, render_template, send_from_directory, abort, redirect, session
from functools import wraps
from werkzeug.security import safe_join
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from cairosvg import svg2png
import mimetypes
import os
import re
from config import *

app = Flask(__name__, static_folder='static/', static_url_path='/')

app.secret_key = os.urandom(128)

mongodb_client = MongoClient(
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port'],
    username=MONGODB_CONFIG['username'],
    password=MONGODB_CONFIG['password']
)

files_collection = mongodb_client[MONGODB_CONFIG['database']][MONGODB_CONFIG['collection']]

def validate_key(key: str) -> bool:
    if not type(key) is str:
        return False
    return bool(re.match(r"^[a-f0-9]{24}$", key))


def convert_svg2png(filename: str):
    new_filename = os.path.splitext(filename)[0] + ".png"
    file_path = safe_join(STORAGE_PATH, filename)
    new_path = safe_join(STORAGE_PATH, new_filename)
    try:
        svg2png(
            url=file_path, write_to=new_path,
            parent_height=1024, parent_width=1024
        )
    finally:
        os.remove(file_path)
    return new_filename


def save_entry(share_key, filename, uploaded_file, published=False):
    file_path = safe_join(STORAGE_PATH, filename)
    uploaded_file.save(file_path)

    file_mimetype = mimetypes.guess_type(file_path)[0]
    if not file_mimetype in ALLOWED_MIME_TYPES:
        os.remove(file_path)
        raise Exception('Invalid MIME type')
    
    created_time = datetime.now().isoformat()
    return files_collection.insert_one({
        'share_key': share_key,
        'filename': filename,
        'created': created_time,
        'updated': created_time,
        'published': published,
        'cleanup_id': session.get('cleanup_id'),
        'search_id': None
    })


def get_entry(share_key, file_id):
    return files_collection.find_one({'_id': ObjectId(file_id), 'share_key': share_key})


def get_entries(share_key, published=True, search=None):
    if not validate_key(share_key):
        return []
    
    if not type(search) is str:
        return files_collection.find({'share_key': share_key, 'published': published})

    return files_collection.find({
        'share_key': share_key, 'published': published,
        '$or': [
            {'filename': {'$regex': search}},
            {'search_id': {'$regex': search}}
        ]
    })


def update_entry(share_key, file_id: str, **kwargs):
    if not get_entry(share_key, file_id):
        return
    files_collection.update_one(
        {'_id': ObjectId(file_id)}, 
        {'$set': {**kwargs, 'updated': datetime.now().isoformat()}}
    )


def delete_entry(file_id):
    entry = files_collection.find({'_id': ObjectId(file_id)})
    files_collection.delete_one({'_id': ObjectId(file_id)})
    filename = entry['filename']
    filepath = safe_join(STORAGE_PATH, filename)
    os.remove(filepath)


def publish_entry(share_key, file_id):
    update_entry(share_key, file_id, published=True, search_id=str(file_id))


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', False):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    cleanup_id = request.form.get('cleanup_id', '')

    if username is None or password is None:
        return render_template('error.html', msg='Bruh have you ever seen a login page before?')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        session['cleanup_id'] = cleanup_id
        return redirect('/')
    
    return render_template('error.html', msg='Lol not a valid cred. Only monke admins allowed!')


@app.route('/', methods=['GET'])
@require_auth
def index():
    return render_template('index.html', share_key=os.urandom(12).hex())


@app.route('/upload', methods=['POST'])
@require_auth
def upload():
    uploaded_file = request.files.get('file', None)
    share_key = request.form.get('share_key', None)

    if uploaded_file is None or share_key is None:
        return render_template('error.html', msg="Apes don't forget to send parameters!")
    
    if not validate_key(share_key):
        return render_template('error.html', msg='Even monkes can whack 24 hexadecimal characters into an input box!')

    share_key = secure_filename(share_key)
    os.makedirs(os.path.join(STORAGE_PATH, share_key), exist_ok=True)

    filename = secure_filename(f"{os.urandom(4).hex()}-{uploaded_file.filename}")
    if filename == '':
        return render_template('error.html', msg='Ya monke! Do you know how to name a file?')
    
    filename = os.path.join(share_key, filename)

    file_ext = os.path.splitext(filename)[1]
    if not file_ext in ALLOWED_FILE_TYPES:
        return render_template('error.html', msg="I throw my poop at a pedestrian each time you don't upload an image")
    
    try:
        saved_entry_id = save_entry(share_key, filename, uploaded_file).inserted_id
    except Exception as _e:
        return render_template('error.html', msg="I throw my poop at a pedestrian each time you don't upload an image")
    if file_ext == '.svg':
        try:
            filename = convert_svg2png(filename)
        except Exception as _e:
            delete_entry(saved_entry_id)
            return render_template('error.html', msg='What the heck mate?!? That SVG was scuffed!')
        update_entry(share_key, saved_entry_id, filename=filename)

    publish_entry(share_key, saved_entry_id)

    return render_template('result.html', link=f'/view/{share_key}/{saved_entry_id}')


@app.route('/flag', methods=['GET'])
@require_auth
def flag():
    return render_template('flag.html', flag=FLAG)


@app.route('/cleanup', methods=['GET'])
@require_auth
def cleanup():
    cleanup_id = session.get('cleanup_id')
    entries = files_collection.find({'cleanup_id': cleanup_id})
    files_collection.delete_many({'cleanup_id': cleanup_id})
    
    total_entries = 0
    for entry in entries:
        filename = entry['filename']
        filepath = safe_join(STORAGE_PATH, filename)
        os.remove(filepath)
        total_entries += 1

    if total_entries > 0:
        os.removedirs(safe_join(STORAGE_PATH, entries[0]['share_key']))
    return "Done"


@app.route('/view/<string:share_key>', methods=['GET'])
def view_folder(share_key):
    if not validate_key(share_key):
        return render_template('error.html', msg='Even monkes can whack 24 hexadecimal characters into an input box!')
    
    search = request.args.get('search', None)
    redirect_to = request.args.get('redirect_to', False)

    entries = get_entries(share_key, search=search)

    if redirect_to:
        try:
            entry_id = entries[0]['_id']
        except Exception as e:
            return abort(404)
        return redirect(f'/view/{share_key}/{entry_id}')
    return render_template('view.html', files=entries)


@app.route('/view/<string:share_key>/<string:file_id>', methods=['GET'])
def view(share_key: str, file_id: str):
    if not validate_key(file_id) or not validate_key(share_key):
        return abort(404)

    file_entry = get_entry(share_key, file_id)
    if file_entry is None:
        return abort(404)
    
    basename = os.path.basename(file_entry['filename'])
    resp = send_from_directory(safe_join(STORAGE_PATH, share_key), basename)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)