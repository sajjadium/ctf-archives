FROM clickhouse/jdbc-bridge:2.1.0
FROM apache/hive:3.1.3
USER root
RUN apt-get update && apt-get install -y unzip wget python3 python3-pip && \
    wget http://files.grouplens.org/datasets/movielens/ml-100k.zip -O /opt/ml-100k.zip && \
    cd /opt && \
    unzip ml-100k.zip && \
    chown -R hive:hive ml-100k && \
    pip3 install pymysql
COPY --from=0 /app/drivers//mysql-connector-java-8.0.28.jar /opt/hive/lib
COPY ./conf/core-site.xml /opt/hadoop/etc/hadoop/core-site.xml
COPY ./conf/hdfs-site.xml /opt/hadoop/etc/hadoop/hdfs-site.xml
COPY ./conf/yarn-site.xml /opt/hadoop/etc/hadoop/yarn-site.xml
COPY ./conf/hive-site.xml /opt/hive/conf/hive-site.xml
COPY ./readflag /readflag
COPY ./init_db.py /init_db.py
COPY ./entrypoint.sh /start.sh
ENTRYPOINT ["/start.sh"]
