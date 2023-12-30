FROM ubuntu@sha256:cbc171ba52575fec0601f01abf6fdec67f8ed227658cacbc10d778ac3b218307
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install socat python3 -y
RUN useradd -m pwn
COPY ./stuff/qjs /home/pwn/
COPY ./stuff/run.py /home/pwn/
COPY ./stuff/readflag /
COPY ./flag.txt /
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn 
RUN chmod 550 /flag.txt
RUN chmod 555 /readflag
RUN chmod u+s /readflag
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:/home/pwn/run.py"]

