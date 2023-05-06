from aiohttp import web

class Server:
    def __init__(self):
        self.app = web.Application()

    def get(self, path, c_type='text/html'):
        def handle(handler):
            decorated_handler = self._handle_factory(handler, c_type)
            self.app.add_routes([web.get(path, decorated_handler)])
        return handle

    def post(self, path, c_type='text/html'):
        def handle(handler):
            decorated_handler = self._handle_factory(handler, c_type)
            self.app.add_routes([web.post(path, decorated_handler)])
        return handle

    def _handle_factory(self, handler, c_type):
        async def decorated_handler(request):
            status, data, headers, *_ = await handler(request) + ({},)
            if status == 200:
                return web.Response(
                    text=data,
                    content_type=c_type,
                    headers=headers
                )
            if status == 302:
                raise web.HTTPFound(location=data)
            return web.Response(text=data, status=status, headers=headers)
        return decorated_handler

    def run(self, host, port):
        web.run_app(self.app, host=host, port=port)
