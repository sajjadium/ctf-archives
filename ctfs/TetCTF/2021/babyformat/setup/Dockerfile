FROM ubuntu:16.04

ARG CHALL

WORKDIR /

ENV CHALLENGE_USER=${CHALL}
ENV CHALLENGE=${CHALL}

RUN apt-get update
RUN apt-get install -y xinetd
RUN useradd -m ${CHALLENGE_USER}

EXPOSE 31337

COPY ./share/. /home/${CHALLENGE_USER}
COPY ./init.sh /init.sh

RUN echo "service ${CHALLENGE}\n{\n\
\tdisable = no\n\
\ttype = UNLISTED\n\
\tport = 31337\n\
\tsocket_type = stream\n\
\tprotocol = tcp\n\
\twait = no\n\
\tuser = ${CHALLENGE_USER}\n\
\tserver = /home/${CHALLENGE_USER}/${CHALLENGE}\n\
\tinstances = 10\n\
}" > /etc/xinetd.d/${CHALLENGE}

RUN chmod 644 /etc/xinetd.d/${CHALLENGE}
RUN chown -R root:${CHALLENGE_USER} /home/${CHALLENGE_USER}/
RUN chmod 755 /home/${CHALLENGE_USER}/${CHALLENGE}
RUN chmod 640 /home/${CHALLENGE_USER}/flag
RUN chmod 755 /init.sh

ENTRYPOINT [ "/init.sh" ]