import hyper
from uuid import uuid4

from config import cfg


def create_connection():
    hyper.tls.cert_loc="./cert.pem"
    return hyper.HTTPConnection(cfg["INTERNAL"]["HOST"], secure=True)

def get_uuid():
    return str(uuid4())