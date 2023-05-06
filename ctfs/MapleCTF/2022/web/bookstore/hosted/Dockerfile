FROM node:16 
COPY init.sql /init.sql
ENV FLAG="maple{test_flag}"
RUN sed -i "s/FLAGE/$FLAG/g" /init.sql
ENV DB_HOST=127.0.0.1
ENV DB_PORT=3306
ENV DB_USER=player
ENV DB_PASS=Player123!
ENV DB_NAME=bookstore
ENV DB_ADMIN_USER=root
ENV DB_ADMIN_PASS=Rooted123!

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y lsb-release
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.23-1_all.deb
RUN dpkg -i mysql-apt-config_0.8.23-1_all.deb
RUN apt-get update
RUN apt-get install -y mysql-server
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000

ENTRYPOINT [ "./init.sh" ]