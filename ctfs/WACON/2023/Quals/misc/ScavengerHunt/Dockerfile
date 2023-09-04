FROM python:3.11.5@sha256:02808bfd640d6fd360c30abc4261ad91aacacd9494f9ba4e5dcb0b8650661cf5

RUN apt-get update
RUN apt-get install -y socat
RUN apt-get clean

RUN adduser --shell /sbin/nologin treasure

COPY ./src/ /home/treasure

RUN pip install -r /home/treasure/requirements.txt
RUN chown -R root:treasure /home/treasure
RUN chmod -R 750 /home/treasure

WORKDIR /home/treasure

CMD ["sh", "run.sh"]
