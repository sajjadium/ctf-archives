FROM ubuntu@sha256:e6173d4dc55e76b87c4af8db8821b1feae4146dd47341e4d431118c7dd060a74
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install socat python3
RUN useradd -m pwn
WORKDIR /home/pwn
COPY ./chall .
COPY generate_directory_tree.py .
RUN python3 generate_directory_tree.py
RUN chown -R root:root /home/pwn
RUN chmod -R 555 /home/pwn
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:'timeout 60 su pwn -c ./chall'"]

