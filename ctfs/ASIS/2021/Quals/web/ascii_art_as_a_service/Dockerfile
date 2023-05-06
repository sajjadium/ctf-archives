FROM ubuntu:21.10

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y 
RUN apt-get install -y nodejs npm jp2a

ENV TERM=xterm
ENV NODE_ENV=production
WORKDIR /app
COPY ./app/ /app/
RUN npm install
RUN chmod +x ./index.js
RUN chmod 777 /app/request
RUN chmod 777 /app/output
RUN useradd -m www
USER www
CMD /app/index.js 2>/dev/null