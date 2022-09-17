FROM ghcr.io/graalvm/graalvm-ce:22.2.0
RUN gu install nodejs python
RUN microdnf install unzip && \
    curl -L https://github.com/wildfly/wildfly/releases/download/26.1.2.Final/wildfly-26.1.2.Final.zip -o /tmp/wildfly.zip && \
    cd /app && unzip /tmp/wildfly.zip && mv wildfly-*.Final/* . && rm -rf wildfly-* /tmp/wildfly.zip
RUN microdnf install nginx
COPY app.war /app/standalone/deployments
RUN touch app.war.dodeploy && \
    rm -rf jabasass && \
    mkdir -p /app/modules/org/graalvm/main
COPY module.xml /app/modules/org/graalvm/main/module.xml

RUN groupadd ctf && \
    useradd -g ctf ctf -m -s /bin/bash && \
    sed -i 's/#\([a-z0-9=]\+\)/\1/' /app/standalone/configuration/mgmt-users.properties && \
    (timeout 10 /app/bin/standalone.sh || true) && \
    sleep 5 && \
    nginx && \
    chmod -R 0777 /app/standalone/data/content && \
    chmod 0777 /app/standalone/deployments && \
    chmod -R 0777 /app/standalone/log && \
    chmod -R 0777 /app/standalone/tmp/ && \
    chmod o+r -R /app/standalone/configuration && \
    chmod o+w /app/standalone/configuration/logging.properties && \
    (mkdir -p /app/standalone/configuration/standalone_xml_history || true) && \
    chmod o+w /app/standalone/configuration/standalone_xml_history #???wtf why need it

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY html /var/www/html
COPY run.sh /run.sh
COPY readflag /readflag
WORKDIR /home/ctf
ENTRYPOINT ["/run.sh"]
