import cherrypy


class Root(object):
    ALLOWED_CHARS = "0123456789+-*/ "

    @cherrypy.expose
    def default(self, *args, **kwargs):
        expr = str(kwargs.get("expr", 42))
        if len(expr) < 50 and all(c in self.ALLOWED_CHARS for c in expr):
            return str(eval(expr))
        return expr


cherrypy.config.update({"engine.autoreload.on": False})
cherrypy.server.unsubscribe()
cherrypy.engine.start()
app = cherrypy.tree.mount(Root())
