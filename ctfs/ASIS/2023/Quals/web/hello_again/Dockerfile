FROM ubuntu@sha256:aabed3296a3d45cede1dc866a24476c4d7e093aa806263c27ddaadbdce3c1054

RUN apt update
RUN apt install wget unzip gcc -y
WORKDIR /tmp
RUN wget https://github.com/oven-sh/bun/releases/download/bun-v1.0.3/bun-linux-x64.zip 
RUN unzip ./bun-linux-x64
RUN cp ./bun-linux-x64/bun /bin/ && mkdir /app/
RUN useradd -M ctf
COPY ./stuff/index.js /app/index.js
COPY ./stuff/cgi-bin /app/cgi-bin
COPY ./stuff/readflag.c /tmp/readflag.c
COPY ./flag.txt /flag.txt
RUN chmod 555 /app/ -R 
RUN gcc -static /tmp/readflag.c -o /readflag
RUN chmod u+s /readflag
RUN chmod 400 /flag.txt
RUN rm /tmp/* -r

USER ctf
CMD ["/bin/bun","/app/index.js"]
