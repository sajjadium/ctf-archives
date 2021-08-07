FROM alpine:latest
RUN apk add rust python3 py-pip libseccomp-dev cargo
RUN python3 -m pip install flask beautifulsoup4 gunicorn

COPY app /app
COPY flag.txt /
WORKDIR /app

RUN mkdir uploads

RUN addgroup -S ctf && adduser -S ctf -G ctf
RUN chown -R ctf:ctf /app && chmod -R 770 /app
RUN chown -R root:ctf /app && \
  chmod -R 770 /app

USER ctf
RUN cd /app/skeleton && cargo build -q
ENTRYPOINT ["/app/start.sh"]
