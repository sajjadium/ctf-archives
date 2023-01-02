import requests
import os, sys
import base64

if sys.version_info.major < 3:
    from urllib import url2pathname
else:
    from urllib.request import url2pathname


# https://stackoverflow.com/questions/10123929/fetch-a-file-from-a-local-url-with-python-requests
class LocalFileAdapter(requests.adapters.BaseAdapter):
    """Protocol Adapter to allow Requests to GET file:// URLs

    @todo: Properly handle non-empty hostname portions.
    """
    @staticmethod
    def _chkpath(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ('put', 'delete'):
            return 501, "Not Implemented"  # TODO
        elif method.lower() not in ('get', 'head'):
            return 405, "Method Not Allowed"
        elif os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):  # pylint: disable=unused-argument
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        @todo: Should I bother filling `response.headers` and processing
               If-Modified-Since and friends using `os.stat`?
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)
        if response.status_code == 200 and req.method.lower() != 'head':
            try:
                response.raw = open(path, 'rb')
            except (OSError, IOError) as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


if __name__ == '__main__':
    try:
        if (len(sys.argv) < 2):
            exit()
        url = sys.argv[1]
        headers = {'user-agent': 'PythonBot/0.0.1'}
        request = requests.session()
        request.mount('file://', LocalFileAdapter())

        # check extentsion
        white_list_ext = ('.jpg', '.png', '.jpeg', '.gif')
        vaild_extension = url.endswith(white_list_ext)

        if (vaild_extension):
            # check content-type
            res = request.head(url, headers=headers, timeout=3)
            if ('image' in res.headers.get("Content-type")
                    or 'image' in res.headers.get("content-type")
                    or 'image' in res.headers.get("Content-Type")):
                r = request.get(url, headers=headers, timeout=3)
                print(base64.b64encode(r.content))
            else:
                print(0)
        else:
            print(0)

    except Exception as e:
        # print e
        print(0)