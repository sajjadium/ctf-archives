FROM ubuntu@sha256:e6173d4dc55e76b87c4af8db8821b1feae4146dd47341e4d431118c7dd060a74
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install socat python3 -y
RUN useradd -m pwn
COPY ./stuff/lua /home/pwn/
COPY ./stuff/run.py /home/pwn/
COPY ./stuff/readflag /
COPY ./flag.txt /
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn 
RUN chmod 550 /flag.txt
RUN chmod 555 /readflag
RUN chmod u+s /readflag
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:/home/pwn/run.py"]
