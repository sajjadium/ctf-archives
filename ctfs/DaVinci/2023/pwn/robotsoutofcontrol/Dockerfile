FROM ubuntu@sha256:b2175cd4cfdd5cdb1740b0e6ec6bbb4ea4892801c0ad5101a81f694152b6c559 AS app

FROM pwn.red/jail

COPY --from=app / /srv

COPY vuln /srv/app/run
COPY flag /srv/app/flag

