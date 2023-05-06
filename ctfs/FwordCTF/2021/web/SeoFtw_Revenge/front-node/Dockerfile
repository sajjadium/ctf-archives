FROM node
RUN useradd ctf
COPY ./index.js /opt/
COPY ./package.json /opt/
WORKDIR /opt/
RUN npm install
USER ctf
CMD ["node","index.js"]
