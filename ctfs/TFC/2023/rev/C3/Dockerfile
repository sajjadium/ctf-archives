FROM swift:latest

RUN /usr/sbin/useradd --no-create-home -u 1000 ctf

WORKDIR /home/ctf

COPY c3 .

RUN chown -R root:root /home/ctf

USER ctf

EXPOSE 1337

ENV FLAG=TFCCTF{test}

CMD /home/ctf/c3

