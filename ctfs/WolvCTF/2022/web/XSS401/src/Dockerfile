# It is tricky to get puppeteer to launch Chrome inside a container.
# This docker image has done all the hard work.  It already has chrome installed,
# but we go ahead and let puppeteer pull down its own version anyway.
FROM markhobson/node-chrome
RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install
COPY ./ ./
ENV FLAG=wsc{redacted}
EXPOSE 80

CMD ["/bin/bash", "start.sh"]