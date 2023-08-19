FROM python:buster
RUN apt-get -qqy update && \
    apt-get -qqy --no-install-recommends install \
    qutebrowser xvfb cron && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN pip install flask

COPY server.py /
RUN echo '#!/bin/sh\necho flag{placeholder}' > /proof_placeholder.sh
RUN echo "#!/bin/sh\nrm -rf /tmp/*" > /cls
RUN chmod 555 /server.py /proof_*.sh /cls
RUN crontab -l | { cat; echo "*/30 * * * * /cls"; } | crontab

WORKDIR /usr/share/javascript/pdf
WORKDIR /tmp
COPY pdfjs-1.10.88-dist.zip .
RUN unzip pdfjs-1.10.88-dist.zip -d pdfjs && \
    mv /tmp/pdfjs/* /usr/share/javascript/pdf && \
    rm -rf /tmp/*
RUN chmod -R 555 /usr/share/javascript/pdf

RUN useradd kyubey --create-home

WORKDIR /tmp
ENV G_SITEKEY placeholder
ENV G_SECRET placeholder
ENV DISPLAY :99
CMD ["bash","-c","cron & Xvfb :99 -screen 0 640x400x8 -nolisten tcp & runuser -u kyubey -- python /server.py"]