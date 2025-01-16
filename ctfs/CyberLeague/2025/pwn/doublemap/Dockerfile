FROM ubuntu:latest

ENV user chall
RUN useradd -m $user

COPY ./ynetd /usr/local/bin/ynetd
COPY ./dist/$user /home/$user/
COPY ./flag /home/$user/

RUN chmod -R 755 /usr/local/bin/ynetd
RUN chown -R root:$user /home/$user
RUN chmod -R 750 /home/$user

USER $user
WORKDIR /home/$user

EXPOSE 10002
CMD ["ynetd", "-p", "10002", "-lp", "20", "./chall"]