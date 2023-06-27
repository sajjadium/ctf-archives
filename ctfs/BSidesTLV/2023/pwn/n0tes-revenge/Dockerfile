FROM debian:12-slim
WORKDIR /usr/src/app

ARG USERNAME=app
ADD flag.txt banner.txt n0tes-revenge /usr/src/app/

ENV IDLE_TIMEOUT=30
ENV SESSION_TIMEOUT=120
ENV COMMAND=/usr/src/app/n0tes-revenge
ENV PROCESS_OPTIONS="pty,setuid=${USERNAME},echo=0,raw,iexten=0"
ENV ADDRESS_OPTIONS="fork,reuseaddr"

RUN set -eux; \
    \
    apt-get update && apt-get install -y socat; \
	\
	chmod +x /usr/src/app/n0tes-revenge; \
    adduser --disabled-password --no-create-home --gecos ${USERNAME} ${USERNAME}

USER ${USERNAME}
ENV HOME=/tmp

EXPOSE 8080
CMD [ "sh", "-c", "socat -dd -t${SESSION_TIMEOUT} -T${IDLE_TIMEOUT} \"TCP4-LISTEN:8080,${ADDRESS_OPTIONS}\" \"EXEC:${COMMAND},${PROCESS_OPTIONS}\"" ]
