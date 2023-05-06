# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t log4sanitycheck .
# 3) docker run -p 1337:1024 --rm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it log4sanitycheck

FROM debian:bullseye

# Install deps.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        default-jre-headless && \
    rm -rf /var/lib/apt/lists/

# Set up the flag
COPY flag.txt docker-stuff/readflag /
RUN chown root:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

# Set up ynetd and the launcher
RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY Vuln.class run.sh *.xml *.jar /home/ctf/
COPY ynetd /sbin/
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/run.sh && \
    chmod 004 /home/ctf/*.class /home/ctf/*.jar /home/ctf/*.xml

# We're paranoid
RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

# Run
USER root
EXPOSE 1024
CMD ynetd -np y -lm -1 -lpid 64 -lt 10 -t 30 "FLAG='$(cat /flag.txt)' /home/ctf/run.sh"
