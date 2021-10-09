FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y \
  coq coq-theories make python3 xinetd

COPY . /app
RUN cp /app/xinetd.conf /etc/xinetd.d/chall

EXPOSE 1337

ENTRYPOINT ["xinetd", "-dontfork"]
