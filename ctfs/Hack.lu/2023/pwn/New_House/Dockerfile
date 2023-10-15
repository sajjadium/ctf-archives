FROM ubuntu

RUN mkdir /chall
ADD flag.txt run.sh ld.so.2 libc.so.6 new_house ynetd /chall/

WORKDIR /chall

CMD ["./run.sh"]

EXPOSE 1337
