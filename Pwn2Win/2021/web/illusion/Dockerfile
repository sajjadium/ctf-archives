FROM node:alpine

EXPOSE 1337

# copy flag
COPY flag.txt /root/flag.txt

# copy readflag binary (it just reads the flag)
COPY readflag /
RUN chmod 4755 /readflag

# install web application
COPY src /app
RUN cd /app && npm install

# change to guest user
USER 405

# run application and stay alive for 5 minutes
COPY entrypoint.sh / 
ENTRYPOINT /entrypoint.sh