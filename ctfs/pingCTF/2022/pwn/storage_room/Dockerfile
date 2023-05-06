FROM python:3

RUN pip3 install flask
COPY ./storage_room /storage_room
RUN echo "ping{REDACTED}" > "/flag-$(head -c 32 /dev/random | sha1sum | cut -d ' ' -f 1 | tr -d '\n')"
RUN useradd --no-create-home --home-dir /home/no_privs --shell /bin/false no_privs
RUN chown root:root /storage_room/ && chmod -R 555 /storage_room/

USER no_privs
WORKDIR /storage_room
CMD [ "python3", "app.py" ]