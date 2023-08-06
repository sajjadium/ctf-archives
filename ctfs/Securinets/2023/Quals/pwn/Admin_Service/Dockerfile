FROM ubuntu@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf

COPY services .
COPY flag .

COPY libseccomp.so.2 .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .

RUN mkdir ./chat
COPY chat ./chat

COPY ynetd .

RUN chmod 777 ./ynetd
RUN chown -R ctf:ctf /home/ctf

USER ctf
CMD ./ynetd -p 1234 ./services 2>/dev/null
