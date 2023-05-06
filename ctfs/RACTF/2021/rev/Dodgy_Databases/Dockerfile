FROM archlinux:latest
WORKDIR /srv

RUN pacman -Sy
RUN pacman --noconfirm -S socat

ADD chal /srv/challenge
ADD database.txt /srv/
RUN chmod +x /srv/challenge

EXPOSE 5000

RUN useradd -M -s /usr/bin/nologin ctf
USER ctf
ENTRYPOINT ["socat", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge,stderr"]
