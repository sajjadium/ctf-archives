import requests
import uuid
from logzero import logger

# create flag user
pw = uuid.uuid4().hex
flag = open('flag', 'rb').read()

logger.info(f'flagger password: {pw}')
s = requests.Session()
r = s.post(f'http://127.0.0.1:1024/registerlogin',
                data={'username': 'flagger','password':pw}, allow_redirects=False)

s.post(f'http://127.0.0.1:1024/add_note',
                data={'body': flag, 'title':'flag'}, allow_redirects=False)