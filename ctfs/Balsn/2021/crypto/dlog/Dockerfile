FROM python:3.9-slim
MAINTAINER sasdf

RUN useradd -m ctf && \
    chmod 774 /tmp && \
    chmod -R 774 /var/tmp && \
    chmod -R 774 /dev && \
    chmod -R 774 /run && \
    chmod 1733 /tmp /var/tmp /dev/shm && \
    echo '[*] Done'

COPY ./src /home/ctf

RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf/server.py && \
    pip install -r /home/ctf/requirements.txt && \
    echo '[*] Done'

EXPOSE 27492
CMD ["/bin/bash", "/home/ctf/run.sh"]
