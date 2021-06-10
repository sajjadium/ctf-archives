# docker build -t pycry .
# docker run -p 5117:5117 -d --name pycry pycry

FROM ubuntu:18.04

RUN apt-get update -y && apt-get install xinetd -y

RUN useradd -m pycry
COPY python flag run.py run.sh /home/pycry/
COPY pylib.tar.gz /home/pycry/
RUN cd /home/pycry && tar xf pylib.tar.gz && rm pylib.tar.gz
COPY xinetd.conf /etc/xinetd.d/pycry

RUN chown -R root:pycry /home/pycry
RUN chmod -R 750 /home/pycry

EXPOSE 5117
ENTRYPOINT ["xinetd", "-dontfork"]
