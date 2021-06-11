from itsdangerous import Signer, base64_encode, base64_decode
from flask import Flask, request, render_template, make_response, g, Response
from flask.views import MethodView

import urlparse
import shutil
import utils
import os
import mimetypes

app = Flask(__name__.split('.')[0])
app.config.from_object(__name__)

BUFFER_SIZE = 128000

URI_BEGINNING_PATH = {
    'authorization': '/login/',
    'weeb': '/weeb/wtf/',
}

def generate_key():
    app.secret_key = os.urandom(24)


def generate_cookie_info(origin=None):

    if not origin:
        origin = request.headers.get('Origin')
    useragent = request.headers.get('User-Agent')
    return '%s %s' % (str(origin), str(useragent))

def verify_cookie(cookey):

    is_correct = False

    cookie_value = request.cookies.get(cookey)
    if cookie_value:
        s = Signer(app.secret_key)
        expected_cookie_content = \
            generate_cookie_info(base64_decode(cookey))
        expected_cookie_content = s.get_signature(expected_cookie_content)

        if expected_cookie_content == cookie_value:
            is_correct = True

    return is_correct

def is_authorized():

    origin = request.headers.get('Origin')
    if origin is None: 
        return True
    return verify_cookie(base64_encode(origin))


@app.before_request
def before_request():

        headers = {}
        headers['Access-Control-Max-Age'] = '3600'
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Allow-Headers'] = \
            'Origin, Accept, Accept-Encoding, Content-Length, ' + \
            'Content-Type, Authorization, Depth, If-Modified-Since, '+ \
            'If-None-Match'
        headers['Access-Control-Expose-Headers'] = \
            'Content-Type, Last-Modified, WWW-Authenticate'
        origin = request.headers.get('Origin')
        headers['Access-Control-Allow-Origin'] = origin

        specific_header = request.headers.get('Access-Control-Request-Headers')

        if is_authorized():
            status_code = 200

        elif request.method == 'OPTIONS' and specific_header:
            headers['Access-Control-Request-Headers'] = specific_header
            headers['Access-Control-Allow-Methods'] = ', '.join(['GET', 'PUT', 'PROPFIND', 'DELETE','COPY', 'MOVE', 'OPTIONS'])
            response = make_response('', 200, headers)
            return response

        else:
            s = Signer(app.secret_key)
            headers['WWW-Authenticate'] = 'Nayookie login_url=' + \
                urlparse.urljoin(request.url_root,
                URI_BEGINNING_PATH['authorization']) + '?sig=' + \
                s.get_signature(origin) + '{&back_url,origin}'
            response = make_response('', 401, headers)
            return response

        g.status = status_code
        g.headers = headers

class weeb(MethodView):
    methods = ['GET', 'PUT', 'PROPFIND', 'DELETE','COPY', 'MOVE', 'OPTIONS']

    def __init__(self):
        self.baseuri = URI_BEGINNING_PATH['weeb']

    def get_body(self):

        request_data = request.data

        try:
            length = int(request.headers.get('Content-length'))
        except ValueError:
            length = 0

        if not request_data and length:
            try:
                request_data = request.form.items()[0][0]
            except IndexError:
                request_data = None
        return request_data

    def get(self, pathname):

        status = g.status
        headers = g.headers
        status = 501

        return make_response('', status, headers)

    def put(self, pathname):
        status = g.status
        headers = g.headers
        status = 501

        return make_response('', status, headers)

    def propfind(self, pathname):
        status = g.status
        headers = g.headers

        pf = utils.PropfindProcessor(
            URI_BEGINNING_PATH['weeb'] + pathname,
            app.fs_handler,
            request.headers.get('Depth', 'infinity'),
            self.get_body())
        try:
            response = make_response(pf.create_response() + '\n', status, headers)
        except IOError, e:
            response = make_response('Not found', 404, headers)

        return response


    def delete(self, pathname):
        status = g.status
        headers = g.headers
        status = 501

        return make_response('', status, headers)

    def copy(self, pathname):
        status = g.status
        headers = g.headers
        status = 501

        return make_response('', status, headers)

    def move(self, pathname):
        status = g.status
        headers = g.headers
        status = 501

        return make_response('', status, headers)

    def options(self, pathname):

        return make_response('', g.status, g.headers)

weeb_view = weeb.as_view('dav')
app.add_url_rule(
    '/weeb/wtf/',
    defaults={'pathname': ''},
    view_func=weeb_view
)

app.add_url_rule(
    URI_BEGINNING_PATH['weeb'] + '<path:pathname>',
    view_func=weeb_view
)

@app.route(URI_BEGINNING_PATH['authorization'], methods=['GET', 'POST'])
def authorize():

    origin = request.args.get('origin')

    if request.method == 'POST':
        response = make_response()
        if request.form.get('continue') != 'true':
            generate_key()
        s = Signer(app.secret_key)
        if s.get_signature(origin) == request.args.get('sig'):
            key = base64_encode(str(origin))
            back = request.args.get('back_url')

            info = generate_cookie_info(origin=origin)
            response.set_cookie(key, value=s.get_signature(info), max_age=None,
                expires=None, path='/', domain=None, secure=True, httponly=True)
        else:
            return 'Something went wrong...'

        response.status = '301' # 
        response.headers['Location'] = '/' if not back else back

    else:
        response = make_response(render_template('authorization_page.html',
                                 cookie_list=[ base64_decode(cookey)
                                               for cookey in
                                               request.cookies.keys()
                                               if verify_cookie(cookey) ],
                                 origin=request.args.get('origin'),
                                 back_url=request.args.get('back_url')))
    return response



if __name__ == '__main__':


    app.fs_path = '/app/'
    app.fs_handler = utils.FilesystemHandler(app.fs_path,
                                             URI_BEGINNING_PATH['weeb'])

    generate_key()
    app.run(host="0.0.0.0")

