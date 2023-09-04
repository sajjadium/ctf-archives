FROM python:3.10

WORKDIR /app
COPY app.py .
COPY flag.txt /flag.txt
COPY files/ files/

RUN pip3 install aiohttp

RUN /usr/sbin/useradd --no-create-home -u 1000 ctf
USER ctf

CMD ["python3", "app.py"]
