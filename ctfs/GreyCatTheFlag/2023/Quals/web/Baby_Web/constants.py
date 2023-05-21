import os

FLAG = os.getenv('FLAG', r'grey{fake_flag}')
COOKIE = {"flag": FLAG}