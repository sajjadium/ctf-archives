from dns.resolver import resolve
from dns.exception import DNSException

from smtplib import SMTP
from functools import lru_cache
from subprocess import Popen

import signal


def handler(sig, frame):
    raise RuntimeError("timeout")
signal.signal(signal.SIGALRM, handler)


Popen(['flask', 'run', '--host=0.0.0.0'])


@lru_cache(maxsize=256)
def get_mx(domain):
    try:
        records = resolve(domain, "MX")
    except DNSException:
        return domain
    if not records:
        return domain
    records = sorted(records, key=lambda r: r.preference)
    return str(records[0].exchange)


class RelayHandler:
    def handle_DATA(self, server, session, envelope):
        mx_rcpt = {}
        for rcpt in envelope.rcpt_tos:
            _, _, domain = rcpt.rpartition("@")
            mx = get_mx(domain)
            if mx is None:
                continue
            mx_rcpt.setdefault(mx, []).append(rcpt)

        signal.alarm(5)
        try:
            for mx, rcpts in mx_rcpt.items():
                print('connetin ', mx)
                with SMTP(mx) as client:
                    client.sendmail(
                        from_addr=envelope.mail_from,
                        to_addrs=rcpts,
                        msg=envelope.original_content,
                    )
        finally:
            signal.alarm(0)
