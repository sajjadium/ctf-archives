FROM python:3.10-slim

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN pip install Flask

WORKDIR /home/ctf

ADD ./challenge/app.py    ./
ADD ./challenge/templates ./templates
RUN chown -R root:ctf ./
RUN chmod -R 550      ./

ENTRYPOINT ["/home/ctf/app.py"]
