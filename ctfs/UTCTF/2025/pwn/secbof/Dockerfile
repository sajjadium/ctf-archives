FROM ubuntu:22.04

RUN apt-get update
RUN apt-get update && apt-get install -y build-essential socat libseccomp-dev

ARG FLAG
ARG USER
ENV USER $USER
ENV FLAG $FLAG

WORKDIR /
COPY start.sh /start.sh


RUN chmod 755 /start.sh && \
    echo "$FLAG" > /flag.txt && \
    chown root:root /flag.txt && \
    chmod 644 /flag.txt

EXPOSE 9000

WORKDIR /
COPY chal /chal
RUN chmod +x /chal

CMD ["/start.sh"]
