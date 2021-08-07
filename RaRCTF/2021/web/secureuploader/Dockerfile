FROM python:3-alpine
RUN  pip install --no-cache-dir flask gunicorn

RUN addgroup -S ctf && adduser -S ctf -G ctf

COPY app /app
COPY flag.txt /flag
WORKDIR /app

RUN chown -R ctf:ctf /app && chmod -R 770 /app
RUN chown -R root:ctf /app && \
  chmod -R 770 /app

USER ctf
ENTRYPOINT ["/app/start.sh"]
