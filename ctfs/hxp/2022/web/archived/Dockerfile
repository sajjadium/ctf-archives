# see docker-compose.yml

# Simplified version of https://github.com/xetus-oss/docker-archiva

FROM eclipse-temurin:8-jdk-alpine

# Add the archiva user and group with a specific UID/GUI to ensure
RUN addgroup --gid 1000 archiva &&\
	adduser --system -u 1000 -G archiva archiva &&\
	apk add bash curl coreutils

# Set archiva-base as the root directory we will symlink out of.
ENV ARCHIVA_HOME /archiva
ENV ARCHIVA_BASE /archiva-data
ENV TEMPLATE_ROOT /archiva-templates
ENV EXTERNAL_DATA_DIRS "data,logs,repositories,conf,temp"

# Add local scripts
ADD docker-stuff /tmp
COPY flag.txt proxy /

# Perform most initialization actions in this layer
# resource retriever
RUN chmod +x /tmp/resource-retriever.sh &&\
    /tmp/resource-retriever.sh &&\
    rm /tmp/resource-retriever.sh
# setup
RUN chmod +x /tmp/setup.sh &&\
    /tmp/setup.sh &&\
    rm /tmp/setup.sh
# proxy
RUN chmod 755 /proxy &&\
    chmod 644 flag.txt

RUN mkdir -p ${ARCHIVA_BASE} &&\
    mkdir -p ${ARCHIVA_BASE}/data &&\
    mkdir -p ${ARCHIVA_BASE}/data/databases &&\
    mkdir -p ${ARCHIVA_BASE}/data/databases/users
RUN if [ -d /tmp/users_prod ] ; then \
        echo '[+] running on server with real admin user (password redacted)' && \
        mv -v /tmp/users_prod/* ${ARCHIVA_BASE}/data/databases/users ; \
    else \
        echo '[+] running locally with debug admin user (password: admin123)' && \
        mv -v /tmp/users/* ${ARCHIVA_BASE}/data/databases/users ; \
    fi

# ensure ownership
RUN chown -R archiva:archiva ${ARCHIVA_BASE}

# Switch to the archiva user
USER archiva

# Use SIGINT for stopping
STOPSIGNAL SIGINT

# Standard web ports exposted
EXPOSE 8081

# Use our custom entrypoint
ENTRYPOINT [ "/entrypoint.sh" ]