FROM ubuntu:20.04

RUN apt update && \
        apt -y upgrade && \
        apt install -y xinetd iproute2 wget 

RUN wget https://root.cern/download/cling/cling_2020-11-05_ROOT-ubuntu2004.tar.bz2 -O cling.tar.bz2 
RUN tar xvf cling.tar.bz2 && mv cling_2020-11-05_ROOT-ubuntu2004 cling

RUN apt install -y build-essential

RUN groupadd -r user && useradd -r -g user user

# files in build are not distributed
COPY ./build/ctf.conf /etc/xinetd.d/ctf
COPY ./build/flag /home/user/flag
COPY ./dist/start.sh /home/user/start.sh
COPY ./dist/chall.c /home/user/chall.c

WORKDIR /home/user

RUN chmod 444 ./flag && \
    chmod 444 ./chall.c && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN mv flag flag-$(md5sum flag | awk '{print $1}')
RUN chown -R root:user /home/user

USER user
EXPOSE 30003

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
