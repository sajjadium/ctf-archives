FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get install -y \
apt-transport-https \
ca-certificates \
curl \
gnupg \
lsb-release && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
echo \
 "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io

RUN curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
chmod +x /usr/local/bin/docker-compose

RUN apt-get install -y socat hashcash xxd at && \
rm -rf /var/lib/apt/lists/*

WORKDIR /opt
COPY launch.sh launch_pow.sh ./

CMD atd && socat -d -d -s TCP-LISTEN:1024,reuseaddr,fork EXEC:'timeout --foreground 360 /opt/launch_pow.sh',stderr
