From apacheignite/ignite:2.15.0-jdk11



RUN apk add curl shadow socat && useradd ctf

COPY readflag /readflag
COPY flag.sh /flag.sh
COPY start.sh /start.sh

COPY default-config.xml /opt/ignite/apache-ignite/config/default-config.xml


RUN chmod +x /flag.sh \
    && chmod +x /start.sh \
    && chmod 4711 /readflag \
    && chown -R ctf:ctf /opt/ignite/ \
    && chmod -R 777 /opt/ignite/ 

CMD '/start.sh'