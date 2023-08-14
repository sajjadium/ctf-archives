import tornado

from models import RegistrationHandler, SendMessageHandler, GetMessageHandler, KeyExchangeHandler, GetPublicValuesHandler, GeKeysHandler

def make_app():
    return tornado.web.Application([
        (r"/register", RegistrationHandler),
        (r"/send", SendMessageHandler),
        (r"/get", GetMessageHandler),
        (r"/keys", KeyExchangeHandler),
        (r"/pubs", GetPublicValuesHandler),
        (r"/initkeys", GeKeysHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    port = 7777
    app.listen(port)
    print("Server running on http://localhost:{}".format(port))
    tornado.ioloop.IOLoop.current().start()
   
