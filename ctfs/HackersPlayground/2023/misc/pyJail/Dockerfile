FROM python:3.11.4

RUN apt-get update
RUN apt-get install -y socat

RUN adduser --shell /sbin/nologin jail

COPY . /home/jail

RUN chown -R root:jail /home/jail
RUN chmod -R 750 /home/jail

WORKDIR /home/jail

ENTRYPOINT ["socat","-v","TCP-LISTEN:9999,reuseaddr,fork,su=jail","EXEC:python jail.py,stderr"]
