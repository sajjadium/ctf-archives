FROM python:3.10-slim


RUN apt-get update && \
apt-get --yes install zstd build-essential python3-dev libmemcached-dev libldap2-dev libsasl2-dev libzbar-dev  ldap-utils tox lcov valgrind && \
apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pygost-5.12.tar.zst .

RUN zstd -d < pygost-5.12.tar.zst | tar xf - && cd pygost-5.12 && python setup.py install

COPY client.py app.py

ENTRYPOINT [ "python" ]

CMD ["app.py"]