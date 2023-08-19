FROM ubuntu:22.04

ENV user user9123
ENV PATH="$PATH:/home/$user"

RUN apt-get update
RUN useradd -b /home/$user $user
WORKDIR /home/$user

COPY myluabox .
COPY luaagent .
COPY flag .

RUN chown -R root:$user .
RUN chmod -R 755 .
RUN chmod -R 444 flag

USER $user

CMD ["myluabox"]