FROM ubuntu@sha256:2d7ecc9c5e08953d586a6e50c29b91479a48f69ac1ba1f9dc0420d18a728dfc5

RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m user && \
    chown -R root:root /home/user && \
    chmod 755 /home/user

COPY share /home/user/
COPY run.sh /

RUN chmod +x /run.sh

WORKDIR /home/user

EXPOSE 1337

ENTRYPOINT ["/run.sh"]
