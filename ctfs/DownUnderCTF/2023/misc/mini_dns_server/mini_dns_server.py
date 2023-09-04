import time
from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, TXT, QTYPE, RCODE


class Resolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        reply.header.rcode = RCODE.reverse['REFUSED']

        if len(handler.request[0]) > 72:
            return reply

        if request.get_q().qtype != QTYPE.TXT:
            return reply

        qname = request.get_q().get_qname()
        if qname == 'free.flag.for.flag.loving.flag.capturers.downunderctf.com':
            FLAG = open('flag.txt', 'r').read().strip()
            txt_resp = FLAG
        else:
            txt_resp = 'NOPE'

        reply.header.rcode = RCODE.reverse['NOERROR']
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(txt_resp)))
        return reply


server = DNSServer(Resolver(), port=8053)
server.start_thread()
while server.isAlive():
    time.sleep(1)
