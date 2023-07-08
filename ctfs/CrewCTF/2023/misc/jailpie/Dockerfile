FROM python:3.11 as chroot

RUN useradd -u 1000 -m ctf
COPY ./share /home/ctf
RUN chown -R root:root /home/ctf
RUN chmod -R 755 /home/ctf

WORKDIR /home/ctf

RUN echo 'dummy{test_flag}' > /home/ctf/flag

CMD /home/ctf/run.sh
