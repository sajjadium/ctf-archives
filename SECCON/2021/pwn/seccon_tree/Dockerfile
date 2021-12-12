FROM ubuntu:20.04


RUN apt update && apt upgrade -y && apt install -y python3.9
RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./env /env
COPY --chown=root:user ./flag /env/flag

WORKDIR /env

RUN chmod -R 444 /env && chmod 755 /env
RUN mv flag flag-$(md5sum flag | awk '{print $1}')

USER user

ENV PYTHONUNBUFFERED=x
CMD ["python3.9", "run.py"]
