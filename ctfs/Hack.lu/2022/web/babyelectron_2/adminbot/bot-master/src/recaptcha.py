import json
import requests


def verify(secret_key, response):
    """Performs a call to reCaptcha API to validate the given response"""
    data = {
        'secret': secret_key,
        'response': response,
    }

    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)

    try:
        result = json.loads(r.text)
    except json.JSONDecodeError as e:
        print('[reCAPTCHA] JSONDecodeError: {}'.format(e))
        return False

    if result['success']:
        return True
    else:
        print('[reCAPTCHA] Validation failed: {}'.format(result['error-codes']))
        return False
