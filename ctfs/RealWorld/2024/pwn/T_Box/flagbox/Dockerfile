FROM ubuntu:22.04

COPY ./echo_hex /echo_hex
RUN chmod +x /echo_hex
COPY ./run.sh /run.sh
COPY ./flag /flag

CMD ["sh", "/run.sh"]
