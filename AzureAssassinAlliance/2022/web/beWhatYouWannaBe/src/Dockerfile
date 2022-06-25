FROM node:latest
# COPY linux_signing_key.pub /tmp
COPY ./app /app
RUN sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list 
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install chromium -y
RUN export PUPPETEER_SKIP_DOWNLOAD='true'
WORKDIR /app
RUN npm config set loglevel=http
RUN npm config set registry https://registry.npm.taobao.org
RUN npm install
ENV password=fakepassword
EXPOSE 8000
RUN adduser actfer
USER actfer
ENTRYPOINT ["node","/app/app.js"]
