import SocketServer
import BaseHTTPServer
import CGIHTTPServer

class ThreadingCGIServer(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
    pass

import sys

server = ThreadingCGIServer(('', 4444), CGIHTTPServer.CGIHTTPRequestHandler)
#
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print "Finished"

