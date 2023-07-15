FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv

COPY chal /srv/app/run
COPY libi_love_ffi.so /srv/app
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run