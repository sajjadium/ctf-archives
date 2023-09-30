FROM ubuntu:22.04

RUN apt-get update && apt-get install socat -y

RUN adduser --home /chall --no-create-home --disabled-password --gecos '' vim
ADD ./chall-files/rust /chall/rust
ADD ./chall-files/vimrc /chall/.vimrc
ADD ./chall-files/flag /flag

WORKDIR /chall
USER vim

CMD ["socat", "-t", "180", "-T", "180", "TCP4-LISTEN:12321,reuseaddr,fork", "EXEC:'/chall/rust -m -n -X',ptmx,stderr"]
