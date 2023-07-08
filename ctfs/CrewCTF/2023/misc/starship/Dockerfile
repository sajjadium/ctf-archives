FROM python:alpine


RUN apk --update add socat

WORKDIR /opt/chal
COPY sandbox.py /opt/chal/sandbox.py
COPY flag.txt /flag.txt

# Securing files
RUN chown -R root:root /opt/chal/

# Securing environ
RUN chmod 700 /bin/* /tmp /dev/shm
RUN chmod 755 /usr/bin/env /bin/sh /usr/bin/nc /bin/cat /usr/bin/wget /usr/bin/groups /usr/bin/id /bin/ls /usr/bin/vi

USER nobody

EXPOSE 5000

CMD socat \ 
      TCP-LISTEN:5000,reuseaddr,fork \ 
      EXEC:"/opt/chal/sandbox.py",stderr
