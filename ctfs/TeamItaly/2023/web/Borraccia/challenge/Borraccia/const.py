import os
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__name__))
PUBLIC_DIR = os.path.join(CURRENT_DIR, "public")
STATIC_DIR = os.path.join(PUBLIC_DIR, "static")
ERROR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "errors")