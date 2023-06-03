from random import choice

def token_hex(value):
    alphabet = 'abcdef0123456789'
    return ''.join(choice(alphabet) for _ in range(5))

def token_bytes(value):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(choice(alphabet) for _ in range(value)).encode()
