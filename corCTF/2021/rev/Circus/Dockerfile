from ubuntu:21.04

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install python3-pip g++ wget curl netcat-traditional openssh-server vim nano strace -y && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip && python3 -m pip install pwntools --no-cache-dir

RUN useradd -ms /bin/bash ubuntu
USER ubuntu
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc
#COPY target/release/solution /home/ubuntu
USER root

RUN mkdir -p /run/sshd


COPY dist /dist
RUN chmod -R 600 /dist
RUN chmod 700 /dist/circus
RUN chmod 700 /dist/run.sh

CMD ["sh", "/dist/run.sh"]

