FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y mariadb-server gettext mariadb-client gcc && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
    chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql && \
    chmod 777 /var/run/mysqld

ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=rootpassword
ENV MYSQL_DB=prepared_db


RUN pip install --no-cache-dir flask mysql-connector-python

RUN useradd -m flask

WORKDIR /app

COPY app.py /app/app.py
COPY templates/ /app/templates/
COPY static/ /app/static/

RUN chown -R root:root /app && \
    chmod -R 755 /app

RUN echo "uoftctf{fake_flag_2}" > /root/flag2.txt && \
    chmod 400 /root/flag2.txt && \
    chown root:root /root/flag2.txt

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN rm /readflag.c
RUN chmod 4755 /readflag

COPY init.sql /root/init.sql
EXPOSE 5000
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
