FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt update
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN pip install Flask Flask-Limiter pycryptodome crc

WORKDIR /home/ctf
ADD ./challenge/app.py    ./
ADD ./challenge/templates ./templates
ADD ./challenge/post      ./post
ADD ./challenge/uwsgi.ini ./
RUN chown -R root:ctf ./
RUN chmod -R 550      ./
RUN chown -R ctf:ctf  ./post
RUN chmod    330      ./post
RUN chown -R root:ctf ./post/a0e402ee09c3c146034ee7d657a11084
RUN chmod -R 550      ./post/a0e402ee09c3c146034ee7d657a11084
