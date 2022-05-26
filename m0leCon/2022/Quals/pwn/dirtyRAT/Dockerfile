FROM ubuntu:21.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat

RUN useradd -ms /bin/bash rat
RUN useradd -ms /bin/bash user

WORKDIR /home/user

COPY ./files/ ./


RUN chown -R user:user /home/user
RUN chmod 644 -R /home/user/chall
RUN chmod 744 -R /home/user/scripts

RUN chown rat:rat /home/user/chall/dirtyRAT
RUN chmod 755 /home/user/chall/dirtyRAT

RUN ls -la chall/
RUN ls -la scripts/

EXPOSE 15000

WORKDIR /home/user
ENTRYPOINT ["/home/user/scripts/entry.sh"]
