# challenge image build
FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -yq --no-install-recommends socat libglib2.0-0 libpthread-stubs0-dev\
    && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd -m user

RUN mkdir /vuln
USER user
COPY run.sh /
COPY vuln /vuln

CMD ["/bin/bash", "/run.sh"]
