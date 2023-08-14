FROM python:3.7-slim

RUN pip3 install pycryptodome py_ecc gmpy2
RUN groupadd -r crypto && useradd -r -u 1001 -g crypto crypto

RUN mkdir -p /home/crypto
RUN chown -R crypto /home/crypto
USER crypto

COPY server.py /home/crypto/
COPY flag.py /home/crypto/
#COPY *.pem /home/crypto/

WORKDIR /home/crypto

EXPOSE 1337

CMD ["python3","/home/crypto/server.py"]