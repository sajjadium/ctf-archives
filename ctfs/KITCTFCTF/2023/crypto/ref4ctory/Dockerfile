# docker build -t ref4ctory . && docker run -p 1337:1337 ref4ctory
FROM alpine:latest

RUN apk add python3 socat
WORKDIR /home/user
ADD main.py main.py
ADD flag.txt flag.txt
RUN adduser -D --gecos "" user
USER user
EXPOSE 1337
ENTRYPOINT ["socat","TCP-LISTEN:1337,fork,reuseaddr" ,"EXEC:'timeout 60 python main.py',pty,stderr"]
