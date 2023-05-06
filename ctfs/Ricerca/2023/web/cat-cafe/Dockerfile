FROM tiangolo/uwsgi-nginx-flask:latest

RUN apt update
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN pip install Flask

WORKDIR /home/ctf
ADD ./app.py    ./
ADD ./images    ./images
ADD ./templates ./templates
ADD ./uwsgi.ini ./
ADD ./flag.txt  ./
RUN chown -R root:ctf ./
RUN chmod -R 550      ./
