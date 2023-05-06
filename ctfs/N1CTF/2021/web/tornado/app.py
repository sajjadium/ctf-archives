import tornado.ioloop
import tornado.web
import builtins
import unicodedata
import uuid
import os
import re

def filter(data):
    data = unicodedata.normalize('NFKD',data)
    if len(data) > 1024:
        return False
    if re.search(r'__|\(|\)|datetime|sys|import',data):
        return False
    for k in builtins.__dict__.keys():
        if k in data:
            return False
    return True

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html",)
    def post(self):
        data = self.get_argument("data")
        if not filter(data):
            self.finish("no no no")
        else:
            id = uuid.uuid4()
            f = open(f"uploads/{id}.html",'w')
            f.write(data)
            f.close()
            try:
                self.render(f"uploads/{id}.html",)
            except:
                self.finish("error")
            os.unlink(f"uploads/{id}.html")

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
    ],compiled_template_cache=False)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
