FROM python:3.8

RUN useradd -m ctf

RUN mkdir -p /chal
WORKDIR /chal
COPY ./flag.txt /chal/flag.txt
COPY ./memes.txt /chal/flag.txt
COPY ./app.py /chal/app.py
COPY ./templates/ /chal/templates/
COPY ./static/ /chal/static/

RUN pip3 install --upgrade --no-cache-dir flask

RUN chown -R root:ctf /chal && \
    chmod -R 750 /chal && \
    chmod -R 740 /chal/flag.txt /chal/templates/* /chal/static/* && \
    rm -rf /home/

USER ctf
WORKDIR /chal
CMD ["/usr/bin/env", "python3", "/chal/app.py"]

EXPOSE 8080
