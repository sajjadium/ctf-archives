FROM ubuntu:18.04


RUN apt-get update && apt-get -y upgrade
RUN useradd -d /home/task/ -m -p task -s /bin/bash task
RUN echo "task:task" | chpasswd

WORKDIR /home/task

COPY main .
COPY flag.txt .
COPY ynetd .
COPY run.sh .
RUN chown -R root:root /home/task
RUN chmod 755 ynetd
RUN chmod 755 main
RUN chmod 777 flag.txt
RUN chmod 755 run.sh

USER task
CMD ["./run.sh"]
