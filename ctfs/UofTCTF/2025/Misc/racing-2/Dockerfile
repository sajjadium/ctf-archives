FROM ubuntu:latest AS app

RUN apt-get update && apt-get install -y gcc openssh-server && rm -rf /var/lib/apt/lists/*

# setup ssh
RUN mkdir /var/run/sshd

# create user
RUN useradd -m -s /bin/bash user

RUN mkdir /home/user/.ssh
RUN echo "user:password" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config

RUN rm -f /home/user/permitted

COPY ./flag.txt /flag.txt
RUN chmod 400 /flag.txt && \
    chown root:root /flag.txt

COPY ./chal.c /challenge/chal.c
RUN gcc /challenge/chal.c -o /challenge/chal
RUN chown root:root /challenge/chal && \
    chmod 4755 /challenge/chal

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D"]
