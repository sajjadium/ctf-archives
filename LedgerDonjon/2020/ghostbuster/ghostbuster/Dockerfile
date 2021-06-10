# ubuntu 18.04
FROM ubuntu@sha256:45c6f8f1b2fe15adaa72305616d69a6cd641169bc8b16886756919e7c01fa48b

RUN apt-get update && apt-get install -qy binutils build-essential gdb less netcat-openbsd net-tools openssh-server socat vim && \
    apt-get install -qy --allow-downgrades libc6=2.27-3ubuntu1.2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/

RUN useradd -d /home/ghostbuster -m ghostbuster -s /bin/bash
RUN chown -R root:root /home/ghostbuster

########################################################################
# ssh configuration, nothing to see here
########################################################################

RUN mkdir /run/sshd

# fancy motd
RUN rm /etc/update-motd.d/10-help-text /etc/update-motd.d/60-unminimize && \
    echo QlpoOTFBWSZTWeGQtaIAAIRbgH+Q+OeAEAAFmnGYBDAA+m2DQEamSaZGgaeiGQinjSEAANAACRIp5TT1PUA0BkAxEFmm2mmgLxECWTIQIOv6nHv0nXFjYDbZQpg/yQ/ytjKkWVEO1CAGLkwqkQjUe6WshIwc0qZWblmdxg1rKqPebuQA0mwFWkbLck5MiNqAQCGDmMGcHuLQKqQSLyYToSNF4kUnGStKkiavrrEh2vWZFZS0SpKG8MvlkhUc2AlEUMMrze1EAmiqSLiM2dsKHg8ZJ21eezQfggAwggBvxuQAffTaNyAHFVy/i7kinChIcMha0QA= | base64 -d | bunzip2 > /etc/update-motd.d/50-motd-news && \
    echo "/etc/update-motd.d/50-motd-news" >> /home/ghostbuster/.bashrc

ADD ./network/ssh.key.pub /root/.ssh/authorized_keys
RUN printf "Match User root\n\tX11Forwarding no\n\tAllowTcpForwarding no\n\tForceCommand /root/ssh-isolation.py" >> /etc/ssh/sshd_config
# required by scp to avoid "unknown user" fatal error
RUN for uid in $(seq 3000 3099); do echo ghostbuster-$uid:x:$uid:$uid::/home/ghostbuster:/bin/bash >>/etc/passwd; done

ADD ./network/ssh-isolation.py /root/ssh-isolation.py

########################################################################
# /ssh configuration
########################################################################

ADD ./network/challenge.sh /home/ghostbuster/challenge.sh
ADD ./ghostbuster /home/ghostbuster/ghostbuster
ADD ./libcheck.so /home/ghostbuster/libcheck.so

WORKDIR /home/ghostbuster
USER ghostbuster

# add "-d" to print debug information
CMD ["socat", "tcp-listen:8888,reuseaddr,fork", "exec:/usr/bin/taskset -c 1 /usr/bin/setarch x86_64 --addr-no-randomize /home/ghostbuster/ghostbuster,stderr"]
