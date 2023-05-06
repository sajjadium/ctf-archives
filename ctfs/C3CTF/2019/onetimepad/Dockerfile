# echo 'hxp{FLAG}' > flag.txt && docker build -t onetimepad . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 31336:1024 onetimepad

FROM debian:buster


RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY onetimepad flag.txt /home/ctf/

#  # Permission
#  7 rwx
#  6 rw-
#  5 r-x
#  4 r--
#  3 -wx
#  2 -w-
#  1 --x
#  0 ---

# sane defaults
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

# TODO: chmod all your files below!
RUN chmod 555 onetimepad && \
    chmod 444 flag.txt && \
    mv flag.txt flag_$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24).txt

# check whitelist of writable files/folders
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

# EXPOSE all your ports
EXPOSE 1024
# TODO: CMD your challenge
CMD ynetd -u ctf /home/ctf/onetimepad
