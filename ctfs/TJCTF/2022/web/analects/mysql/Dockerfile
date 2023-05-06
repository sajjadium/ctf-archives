FROM mysql:8.0.28-debian

COPY init/* /docker-entrypoint-initdb.d/
COPY conns.conf /etc/mysql/conf.d/

ENV MYSQL_ROOT_PASSWORD=5f953685870edac8b0c652144ce7f3831c2ac346e4065c38f9c23dc53fc4a9a0
CMD [ "--character-set-server=gb18030" ]
