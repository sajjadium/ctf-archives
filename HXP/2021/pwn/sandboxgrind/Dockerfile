# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t sandboxgrind .
# 3) docker run -p 9001:1024 --rm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it sandboxgrind

# Move to a new, leaner container for the challenge
FROM debian:bullseye

# Copy the sandbox
COPY /sandboxgrind-build.tar.gz /
RUN tar -xzf /sandboxgrind-build.tar.gz && \
    rm /sandboxgrind-build.tar.gz && \
    chown -R root:root /sandboxgrind/ && \
    chmod -R a-w,ug-rx /sandboxgrind/

# Set up ynetd
RUN useradd --create-home --shell /bin/bash ctf
COPY ynetd /sbin/
RUN chmod 555 /home/ctf/ && \
    chown -R root:root /home/ctf/ && \
    chmod 500 /sbin/ynetd

# Set up flag
COPY flag.txt docker-stuff/readflag /
RUN chown root:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

# Set up submission environment
COPY submission.sh /home/ctf/
RUN chmod 005 /home/ctf/submission.sh

# We're paranoid
RUN chmod 1703 /tmp
RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

# Run
USER root
WORKDIR /home/ctf
EXPOSE 1024
CMD ynetd -np y -lm -1 -lt 10 -t 15 -sh n -lpid 16 /home/ctf/submission.sh & \
    while true; do sleep 20s; find /tmp/ -type f -cmin +1 -delete; done
