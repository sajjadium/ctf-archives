FROM python:alpine

RUN apk update
RUN apk add socat

RUN adduser -D ctf -u 1000 -g 1000

### diretory setting
COPY --chown=ctf:ctf server.py /home/ctf/server.py
COPY --chown=ctf:ctf secret.py /home/ctf/secret.py
COPY --chown=ctf:ctf flag.py /home/ctf/flag.py

USER ctf

RUN pip install --upgrade pip
RUN pip install pycryptodome sympy

EXPOSE 5000

CMD ["/usr/bin/socat", "tcp-listen:5000,reuseaddr,fork", "exec:\"python /home/ctf/server.py\""]
