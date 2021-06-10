import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLAG = os.environ.get("FLAG")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY") 
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY") 