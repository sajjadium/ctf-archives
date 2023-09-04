FROM selenium/standalone-chrome

USER root
RUN apt update && apt install -y python3-pip

COPY ./requirements.txt /monkebot/requirements.txt
RUN pip3 install -r /monkebot/requirements.txt

COPY . /monkebot
RUN /usr/sbin/useradd --no-create-home -u 1000 www-monke
USER www-monke
WORKDIR /monkebot

CMD ["python3", "/monkebot/main.py"]