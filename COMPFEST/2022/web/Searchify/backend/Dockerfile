FROM python:3-alpine

COPY flag.txt /REDACTED
COPY src /opt/searchify
COPY patch.sh /tmp/patch.sh

RUN pip install -r /opt/searchify/requirements.txt
RUN /tmp/patch.sh
RUN rm /tmp/patch*

WORKDIR /opt
USER nobody

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]
