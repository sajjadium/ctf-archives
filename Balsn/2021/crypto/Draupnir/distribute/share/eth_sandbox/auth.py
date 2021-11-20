from uuid import uuid4

def load_auth_key():
    with open("/tmp/auth", "r") as f:
        return f.read()

def generate_auth_key():
    auth_key = str(uuid4())
    with open("/tmp/auth", "w") as f:
        f.write(auth_key)
    return auth_key
