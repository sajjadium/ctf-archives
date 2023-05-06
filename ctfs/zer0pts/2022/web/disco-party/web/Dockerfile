FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt -y upgrade
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

ADD ./secret.py ./
ADD ./uwsgi.ini ./
ADD ./static    ./static
ADD ./templates ./templates
ADD ./app.py    ./

RUN chown -R root:ctf ./
RUN chmod -R 555      ./
