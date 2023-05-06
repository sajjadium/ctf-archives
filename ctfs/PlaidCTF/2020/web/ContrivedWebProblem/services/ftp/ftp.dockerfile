FROM node:10

WORKDIR /ppp
RUN mkdir -p /ftp/root/
RUN yarn global add ftp-srv

CMD ["ftp-srv", "-r", "/ftp/root/", "--pasv_url", "172,32,0,21", "ftp://0.0.0.0:21"]