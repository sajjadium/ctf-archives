FROM selenium/standalone-chrome

USER root
RUN apt update && apt install -y python3-pip

COPY ./requirements.txt /adminbot/requirements.txt
RUN pip3 install -r /adminbot/requirements.txt

COPY . /adminbot
RUN /usr/sbin/useradd --no-create-home -u 1000 www-admin
USER www-admin
WORKDIR /adminbot

CMD ["python3", "/adminbot/main.py"]