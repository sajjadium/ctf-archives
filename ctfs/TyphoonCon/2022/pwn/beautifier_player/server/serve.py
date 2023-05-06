#!/usr/bin/env python

from operator import truediv
from aiohttp import web
from PIL import Image, ImageEnhance
from io import BytesIO as buffio
from base64 import b64encode as b64
from os import remove, getenv, makedirs, path
from filelock import FileLock
from time import time

application = web.Application()
routes = web.RouteTableDef()

class logger:

    @staticmethod
    def log_success(message):
        print("[+] %s" % message, flush=True)

    @staticmethod
    def log_info(message):
        print("[!] %s" % message, flush=True)

    @staticmethod
    def log_error(message):
        print("[-] %s" % message, flush=True)

uploads = getenv("uploads", None)
if not uploads or not path.isdir(uploads):
    logger.log_info("You have to set the $uploads with a valid directory")
    uploads = "/tmp/uploads"
    makedirs(uploads, exist_ok=True)

class upload:

    def __init__(self, size):
        lock_file = path.join(uploads, "uploads.lck")
        self.__lock = FileLock(lock_file)
        self.__lock.acquire()
        time_stamp = int(time())
        while True:
            image_path = path.join(uploads, "upload_%x" % time_stamp)
            if not path.isfile(image_path): break
            time_stamp += 1
        self.__path = image_path
        self.__file = open(image_path, "wb+")
        self.__lock.release()
        self.__file.truncate(size)
        
    @property
    def fd(self): return self.__file

    def __del__(self):
        self.__lock.acquire()
        self.__file.close()
        remove(self.__path)
        self.__lock.release()

@routes.post('/submit')
async def server_submit(request):

    content_type = request.headers.get("Content-Type", None)
    content_length = request.headers.get("Content-Length", None)

    if not content_type or not content_type.startswith("image/"):
        return web.Response(text="Only images can be submitted.", status=415)

    if not content_length or not content_length.isnumeric():
        content_length = 2 ** 10

    content_length = int(content_length)
    if content_length > 10 * (2 ** 20):
        return web.Response(text="The maximum file size is 10MB.", status=400)
    logger.log_info("Processing a new image with size %d bytes" % content_length)

    file = upload(content_length)
    async for data in request.content.iter_any():
        file.fd.write(data)
        file.fd.flush()
    file.fd.seek(0)

    buffer = buffio()
    try:
        image = Image.open(file.fd)
        image = ImageEnhance.Contrast(image).enhance(2)
        image.save(buffer, format='PNG')
    except Exception as e:
        logger.log_error("Image processing exception: %s" % str(e))
        return web.Response(text="Unable to process the image.", status=500)
    
    buffer = buffer.getvalue()
    buffer = b"data:image/png;charset=utf-8;base64," + b64(buffer)

    return web.Response(body=buffer)

@routes.get('/')
async def server_upload(request):

    user_agent = request.headers.get("User-Agent", "<unknown>")
    logger.log_success("Connected to a new client: %s" % user_agent)

    uploader = open(path.join(path.abspath(path.dirname(__file__)),
        "static/upload.html"), "r")
    return web.Response(text=uploader.read(), content_type='text/html')
    
def run(host, port):

    try: web.run_app(application, host=host, port=int(port))
    except Exception as e: logger.log_error(str(e))

def main():

    from sys import argv
    if len(argv) != 3:
        logger.log_info("%s <server_host> <server_port>" % argv[0])
        return

    logger.log_info("Starting the server on http://%s:%s" % (argv[1], argv[2]))
    run(argv[1], argv[2])

application.add_routes(routes)
if __name__ == '__main__':
    main()