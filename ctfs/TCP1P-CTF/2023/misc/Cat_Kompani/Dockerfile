FROM ubuntu:lunar

EXPOSE 19010

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt-get install python3 socat -y

COPY src/cat /bin/cat
RUN chown root:root /bin/cat
RUN chmod +s /bin/cat

RUN mkdir /ctf

COPY src/chall.py /ctf/chall.py
RUN chmod +x /ctf/chall.py

COPY src/flag.txt /flag
RUN chown root:root /flag
RUN chmod 400 /flag

RUN chown -R 555 /ctf/
WORKDIR /ctf

RUN rm -rf /bin/bash /bin/dash /usr/bin/bash /usr/bin/dash

CMD ["socat", "TCP-LISTEN:19010,reuseaddr,fork","EXEC:/ctf/chall.py,su=nobody"]