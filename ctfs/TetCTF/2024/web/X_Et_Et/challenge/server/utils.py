from uuid import UUID
import json
import requests


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def is_valid_captcha(secret, captcha):
    if secret == "":
        return True
    else:
        return verify(secret, captcha)


def verify(secret_key, response):
    payload = {'response': response, 'secret': secret_key}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']
    