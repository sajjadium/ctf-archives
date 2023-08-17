# docker build -t honk-honk . && docker run --rm -it -p1024:1024 honk-honk
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ctf@127.0.0.1 -p 1024
FROM ubuntu:latest

RUN apt-get update

RUN apt install ca-certificates gnupg -y
RUN gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list

RUN set -x && \
    apt-get update && \
    apt-get install -y xinetd cmake build-essential unzip git dropbear rsync openssh-client libcap2-bin mono-devel  && apt-get clean

RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf

WORKDIR /home/ctf

# Starts dropbear SSH
COPY run.sh .

# Wraps mono call, setuid script
COPY run_wrapper.c .
RUN gcc run_wrapper.c -o run_wrapper

# Copy CatRunner binaries
RUN mkdir -p /opt/pluginmanager/
COPY bin /opt/pluginmanager/bin/

# Setuid run_cat.sh and do other protections
RUN chmod 755 run_wrapper && chmod u+s run_wrapper && chmod 744 /opt/pluginmanager/bin/CatRunner.exe && chmod 777 /opt/pluginmanager/bin/plugins

# Copy flag and chmod it
COPY flag /
RUN chmod 600 /flag

EXPOSE 1024

# Go! :)
CMD ["/bin/sh","/home/ctf/run.sh"]
