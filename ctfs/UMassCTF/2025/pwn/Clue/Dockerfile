FROM docker.io/ubuntu:20.04

WORKDIR /home/ctf

ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -d /home/ctf -u 1001 ctf
RUN echo "root:dfueisarjcxnzklfhauis" | chpasswd
RUN echo "ctf:reuignbvcnjiofdsanjvnjo" | chpasswd

COPY --chown=root:root assets ./

ENTRYPOINT [ "./ynetd", "-p", "4444", "-u", "ctf", "/home/ctf/clue" ]