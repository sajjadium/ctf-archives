FROM node:16.3-alpine

WORKDIR /app
COPY app/ /app/

RUN npm install
RUN npm install -g forever

# Set non root user
RUN adduser -D user -h /home/user -s /bin/bash user
RUN chown -R user:user /home/user
RUN chmod -R 755 .

USER user
ENV HOME /home/user

EXPOSE 3000
CMD [ "npm", "start"]