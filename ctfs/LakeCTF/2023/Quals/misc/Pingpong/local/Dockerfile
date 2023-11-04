FROM ubuntu:22.04
RUN apt-get update && apt-get install -y netcat mawk 
WORKDIR /home/ctf
COPY players /home/ctf/players
COPY message.txt /tmp/message.txt

CMD ["bash","players/run.sh"]