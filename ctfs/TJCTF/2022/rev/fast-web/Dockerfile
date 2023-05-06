FROM ubuntu:focal-20220113

COPY app ./goahead/server /app/

CMD ["/app/server", "-v", "/app/files/", ":80", "/app/auth.txt", "/app/route.txt"]
