FROM busybox

COPY files/ /tmp/

RUN cat /tmp/config.txt

RUN rm -rf /tmp/

CMD [ "ps", "faux" ]