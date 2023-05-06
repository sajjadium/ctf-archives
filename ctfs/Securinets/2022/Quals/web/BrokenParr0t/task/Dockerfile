From openjdk:11

RUN useradd ctf \
    && mkdir /opt/app

COPY ./task/stackoverctf.jar /opt/app
COPY ./task/flag.txt /
COPY ./task/start.sh /opt/app
WORKDIR /opt/app

USER ctf
ENTRYPOINT ["/opt/app/start.sh"]
