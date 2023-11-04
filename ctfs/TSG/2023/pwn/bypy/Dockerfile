FROM python:3.12.0-bullseye

RUN apt update && \
        apt -y upgrade && \
        apt install -y xinetd iproute2 
RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./build/flag /home/user/flag
COPY --chown=root:user ./src/start.sh /home/user/start.sh
COPY --chown=root:user ./src/executor.py /home/user/executor.py

WORKDIR /home/user

RUN chown -R root:user /home/user
RUN mv flag flag-$(md5sum flag | awk '{print $1}')

USER user

ENV PYTHONUNBUFFERED=x
CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
