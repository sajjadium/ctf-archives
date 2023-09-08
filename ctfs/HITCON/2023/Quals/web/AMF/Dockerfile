FROM python:slim

RUN pip install Py3AMF

RUN useradd -m ctf
COPY server.py /app/server.py
RUN chown -R root:root /app && chmod -R 555 /app

RUN apt-get update && apt-get install -y gcc
COPY readflag.c /readflag.c
COPY flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

USER ctf
EXPOSE 5000

CMD ["python", "/app/server.py"]


