FROM mysql:8.0.31

ENV MYSQL_ROOT_PASSWORD=realworldctf MYSQL_DATABASE=web
COPY my.cnf /etc/mysql/
COPY flag.sql /docker-entrypoint-initdb.d/
COPY web.sql /docker-entrypoint-initdb.d/