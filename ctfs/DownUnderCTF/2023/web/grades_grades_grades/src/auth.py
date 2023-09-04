import jwt
from flask import request, jsonify, current_app, make_response
from functools import wraps
import secrets

SECRET_KEY = secrets.token_hex(32)

def create_token(data):
    token = jwt.encode(data, SECRET_KEY, algorithm='HS256')
    return token

def token_value(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return decoded_token['stu_num'], decoded_token['stu_email'], decoded_token.get('is_teacher', False)

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None

def is_teacher_role():
    # if user isn't authed at all
    if 'auth_token' not in request.cookies:
        return False
    token = request.cookies.get('auth_token')
    try:
        data = decode_token(token)
        if data.get('is_teacher', False):
            return True
    except jwt.DecodeError:
        return False
    return False 


def is_authenticated():
    # if user isn't authed at all
    if 'auth_token' not in request.cookies:
        return False

    token = request.cookies.get('auth_token')
    
    try:
        if jwt.decode(token, SECRET_KEY, algorithms=['HS256']) is not None:
            return True
    except jwt.DecodeError:
        return False
    return False 

def requires_teacher(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = decode_token(token)
            if data is None or data.get("is_teacher") is None:
                return jsonify({'message': 'Invalid token'}), 401
            if data['is_teacher']:
                request.user_data = data
            else:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated

def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = decode_token(token)
            if data is None:
                return jsonify({'message': 'Invalid token'}), 401
            request.user_data = data
        except jwt.DecodeError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
