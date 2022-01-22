FROM ubuntu:18.04

ENV JDK_TAR_GZ="jdk-8u311-linux-x64.tar.gz" \
    TOMCAT_ZIP="apache-tomcat-9.0.56.zip" \
    JAVA_HOME="/opt/jdk" \
    CATALINA_HOME="/opt/tomcat"

COPY ${JDK_TAR_GZ} /opt/
COPY ${TOMCAT_ZIP} /opt/
COPY ROOT.war /opt/
COPY flag /flag
COPY readflag /readflag

RUN set -ex && apt-get update \
    && apt-get install -y lib32z1 zip acl \
    && cd /opt/ \
    && mkdir -p ${JAVA_HOME} \
    && tar xzf ${JDK_TAR_GZ} -C ${JAVA_HOME} --strip-components=1 \
    && update-alternatives --install /usr/bin/java java /opt/jdk/bin/java 100 \
    && update-alternatives --install /usr/bin/javac javac /opt/jdk/bin/javac 100 \
    && update-alternatives --install /usr/bin/jar jar /opt/jdk/bin/jar 100 \
    && rm -rf ${JDK_TAR_GZ} \
    && unzip ${TOMCAT_ZIP} \
    && rm -rf ${TOMCAT_ZIP} \
    && mv *-tomcat-* ${CATALINA_HOME} \
    && cd ${CATALINA_HOME} \
    && rm -rf webapps/* \
    && rm -rf conf/Catalina/localhost/* \
    && rm -rf server/webapps/* \
    && groupadd ctf && useradd -g ctf ctf \
    && chgrp -R ctf ${CATALINA_HOME} \
    && chmod g+w webapps/ logs/ work/ temp/ \
    && chmod g+s webapps/ logs/ work/ temp/ \
    && setfacl -d -m group:ctf:rwx ${CATALINA_HOME}/webapps ${CATALINA_HOME}/work ${CATALINA_HOME}/temp ${CATALINA_HOME}/logs \
    && chmod ug+x bin/*.sh \
    && su ctf -c "cp /opt/ROOT.war webapps/ROOT.war" \
    && rm /opt/ROOT.war \
    && chmod u=srx,g=rx,o=rx /readflag \
    && chmod 400 /flag \
    && rm -rf /var/lib/apt/lists/*

CMD su ctf -c "sh ${CATALINA_HOME}/bin/catalina.sh run"
