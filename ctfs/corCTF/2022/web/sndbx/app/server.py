import manager
import config

from gevent import ssl
from gevent.pywsgi import WSGIServer
from app import app

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('certs/.root/cert.pem', 'certs/.root/priv.pem')

def sni_callback(socket, sni, ctx):
	if sni is None:
		return

	if sni == config.DOMAIN:
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.load_cert_chain('certs/.root/cert.pem', 'certs/.root/priv.pem')

		socket.context = context
		return

	subdomain = sni.split('.')[0]

	if subdomain not in manager.subdomains or sni != f'{subdomain}.{config.DOMAIN}':
		return socket.close()

	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(f'certs/{subdomain}/cert.pem', f'certs/{subdomain}/priv.pem')

	socket.context = context

context.sni_callback = sni_callback

http_server = WSGIServer(('0.0.0.0', config.PORT), app, ssl_context=context)
http_server.serve_forever()
