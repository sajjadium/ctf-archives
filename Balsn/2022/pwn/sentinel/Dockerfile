from ubuntu:jammy
MAINTAINER James

RUN apt-get update && \
    apt-get install ca-certificates curl gnupg lsb-release -qy && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin xinetd -qy

RUN apt-get install python3 -qy

RUN curl -fsSL https://github.com/docker/compose/releases/download/1.29.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

RUN useradd -m sentinel
RUN usermod -aG docker sentinel

RUN chown -R root:root /home/sentinel

ENTRYPOINT ["/init"]
