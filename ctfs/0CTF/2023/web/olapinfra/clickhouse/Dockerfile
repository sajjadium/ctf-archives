FROM clickhouse/jdbc-bridge:2.1.0
FROM clickhouse/clickhouse-server:23.8.4.69
COPY --from=0 /app /app
COPY --from=0 /opt/java/openjdk /opt/java/openjdk
COPY readflag /readflag
COPY hdfs-site.xml /etc/clickhouse-server/
COPY init.sql /docker-entrypoint-initdb.d/init.sql
ENV JDBC_BRIDGE_HOME /app
ENV JAVA_HOME /opt/java/openjdk
ENV LIBHDFS3_CONF /etc/clickhouse-server/hdfs-site.xml
ENV PATH $JAVA_HOME/bin:$PATH
ENV JAVA_TOOL_OPTIONS -XX:+IgnoreUnrecognizedVMOptions -XX:+IdleTuningGcOnIdle -Xshareclasses:name=openj9_system_scc,cacheDir=/opt/java/.scc,readonly,nonFatal


COPY ./entrypoint.sh /start.sh
ENTRYPOINT ["/start.sh"]
