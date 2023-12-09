FROM ubuntu@sha256:b5d5cddaeb8d2f150660cf8f9a1203dd450ac765e6c07630176ac6486eceaddb

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-server python3 python3-pwntools tini # cron 

# Configure SSHd
RUN mkdir /var/run/sshd

# Configure users
RUN useradd chall -s /bin/bash
RUN useradd -M chall-pwned
RUN echo 'chall:chall' | chpasswd
RUN passwd -d chall-pwned
RUN userdel ubuntu

# Add cronjob to clean /tmp every 5 minutes 
# RUN crontab -l | { cat; echo "* * * * * rm -rf /tmp/*"; } | crontab -

# Setup challenge
WORKDIR /home/chall

COPY bot .
COPY answers.txt . 
COPY flag.txt . 

# Set permissions
RUN chown chall-pwned bot && chmod 4555 bot
RUN chown chall-pwned flag.txt && chmod 400 flag.txt
RUN chown chall-pwned answers.txt && chmod 400 answers.txt

# Hide very private answer files from others
RUN chmod 733 /tmp

ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["sh", "-c", "cron start && /usr/sbin/sshd -D"]
CMD ["/usr/sbin/sshd", "-D"]
