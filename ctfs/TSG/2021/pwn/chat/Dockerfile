FROM ubuntu:20.04

RUN apt update && \
        apt -y upgrade && \
        apt install -y python3

RUN groupadd -r user && useradd -r -g user user

COPY ./client /client
COPY ./host /host
COPY ./connector.py /connector.py
COPY ./flag /flag

RUN chmod 444 /flag && \
    chmod 555 /host && \
    chmod 555 /client && \
    chmod 555 /connector.py

RUN mv flag flag-$(md5sum flag | awk '{print $1}')

USER user
EXPOSE 30001

ENTRYPOINT ["python3","-u", "connector.py"]
