import re


def validate_registration(form_data):
    if not form_data['username'] or not form_data['password']:
        return 'missing parameter'
    if not re.match(r'^[a-zA-Z0-9-_$]+$', form_data['username']):
        return 'do you have special characters in your name??'
    if len(form_data['username']) > 30:
        return 'username too long'
    if len(form_data['username']) < 4:
        return 'username too short'
    if len(form_data['password']) > 30:
        return 'password too long'
    if len(form_data['password']) < 4:
        return 'password too short'
    return None


def validate_login(form_data):
    if not form_data['username'] or not form_data['password']:
        return 'missing parameter'


def validate_note(form_data):
    if not form_data['title'] or not form_data['body']:
        return 'missing parameter'
    if len(form_data['title']) > 80:
        return 'title too long'
    if len(form_data['title']) < 1:
        return 'title too short'
    if len(form_data['body']) > 200:
        return 'body too long'
    if len(form_data['body']) < 1:
        return 'body too short'
    return None
