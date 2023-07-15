FROM node:16
COPY ./* /home/node/app/
WORKDIR /home/node/app
RUN npm install --force
ENV PORT=8081
CMD ["npm", "start"]
EXPOSE 8081