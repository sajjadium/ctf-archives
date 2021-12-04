FROM debian:buster-20200803

RUN mkdir -p /server && mkdir /server/content

ADD server /server
ADD flag.txt /server
ADD init.sh /bin
ADD index.html /server/content

RUN groupadd -r server && useradd -r -g server server -d /server && \
    chown -R root:server /server && \
    chmod 750 /server/server && \
    chmod 440 /server/flag.txt && \
	chmod 755 /bin/init.sh && \
	chmod 770 /server/content && \
	chmod 744 /server/content/index.html

USER server
ENTRYPOINT [ "/bin/init.sh" ]

