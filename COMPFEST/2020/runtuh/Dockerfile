FROM nsjail
# forked from https://github.com/google/nsjail

RUN mkdir /app && apt-get update && apt-get install lib32z1 -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY files/runtuh .
COPY files/flag.txt .
RUN chmod 555 runtuh
RUN chmod 444 flag.txt

COPY nsjail.sh /
RUN chmod 555 /nsjail.sh
ENTRYPOINT ["/nsjail.sh"]
CMD ["runtuh"]
