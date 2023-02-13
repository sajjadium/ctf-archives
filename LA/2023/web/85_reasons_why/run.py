#! /usr/bin/env python

import os
from dotenv import load_dotenv

load_dotenv()

from app import app

def main():
    port = os.getenv('PORT') 
    if port != 0:
        app.run(host='127.0.0.1', port=port)
    else:
        app.run()


if __name__ == '__main__':
    main()
