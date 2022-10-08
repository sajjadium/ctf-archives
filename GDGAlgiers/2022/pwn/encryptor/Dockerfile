FROM ubuntu:22.04@sha256:20fa2d7bb4de7723f542be5923b06c4d704370f0390e4ae9e1c833c8785644c1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python-is-python3 python3-pip --no-install-recommends
RUN python -m pip install -U pip

RUN useradd -m -d /home/encryptor -s /bin/bash -u 1000 encryptor

WORKDIR /home/encryptor

COPY ./challenge/encryptor-0.0.1-cp310-cp310-linux_x86_64.whl ./
RUN python -m pip install ./encryptor-0.0.1-cp310-cp310-linux_x86_64.whl

COPY ./challenge/flag.txt ./

RUN chown -R root:encryptor /home/encryptor && \
    chmod 750 /home/encryptor && \
    chown root:encryptor /home/encryptor/flag.txt && \
    chmod 440 /home/encryptor/flag.txt

COPY ./challenge/entrypoint.sh ./
COPY ./challenge/run_server.py ./
RUN chmod +x /home/encryptor/entrypoint.sh

EXPOSE 1337
USER encryptor
CMD ["/home/encryptor/entrypoint.sh"]
