FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-bottle && apt-get clean
RUN useradd -d /home/ctf -m ctf

WORKDIR /home/ctf

COPY ./dist/ /home/ctf/
RUN chown ctf:ctf film.db

USER ctf
EXPOSE 8080/tcp
CMD python3 web.py
