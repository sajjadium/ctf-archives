FROM ubuntu:22.04 as ubuntu

RUN useradd -m user
RUN apt update -y
RUN apt install socat -y

COPY llm_wrapper /home/user/
COPY flag.txt /home/user/

WORKDIR "/home/user/"

RUN chown -R root:root . && \
    chmod o+rx . && \
    chmod 444 flag.txt && \
    chmod a+x llm_wrapper

USER user

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/user/llm_wrapper"
