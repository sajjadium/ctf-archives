FROM node:12
RUN mkdir -p /ctf/app
WORKDIR /ctf/app
COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install
COPY ./ ./
EXPOSE 80

CMD ["/bin/bash", "start.sh"]