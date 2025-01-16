FROM ubuntu:latest

ENV user bo
RUN useradd -m $user

COPY ./ynetd /usr/local/bin/ynetd
COPY ./dist/$user /home/$user/
COPY ./flag.txt /home/$user/

RUN chmod -R 755 /usr/local/bin/ynetd
RUN chown -R root:$user /home/$user
RUN chmod -R 750 /home/$user

USER $user
WORKDIR /home/$user

EXPOSE 10001
CMD ["ynetd", "-p", "10001", "-lp", "20", "./bo"]
