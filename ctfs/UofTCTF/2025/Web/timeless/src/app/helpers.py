import os
import hashlib
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}
def allowed_username(username):
    return ".." not in username
def allowed_file(filename):
    return not ("." in filename and (filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS or ".." in filename))

def gen_filename(username, filename, timestamp=None):
    if not timestamp:
        timestamp = int(datetime.now().timestamp())
    hash_value = hashlib.md5(f"{username}_{filename}_{timestamp}".encode()).hexdigest()
    return hash_value

def ensure_upload_directory(base_path, username):
    if not allowed_username(username):
        return None
    user_directory = os.path.join(base_path, username)
    if os.path.exists(user_directory):
        return user_directory
    os.makedirs(user_directory, exist_ok=True)
    return user_directory
