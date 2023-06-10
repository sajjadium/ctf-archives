import random
import string
import jwt

def random_string(k=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

def parse_token(token, secret):
    data = jwt.decode(token, secret, algorithms = 'HS256')

    try:
        status = data['status']
        transaction_id = data['transaction_id']
    except KeyError as err:
        raise jwt.DecodeError()

    return transaction_id, status
