FROM ubuntu:21.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release xdg-utils  wget curl gnupg python python3-pip unixodbc-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/ubuntu/21.04/prod.list > /etc/apt/sources.list.d/mssql-release.list


RUN apt-get update 
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install Flask pyodbc selenium flask-session

WORKDIR /tmp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -q
RUN dpkg -i ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

ENV TERM=xterm
ENV NODE_ENV=production
WORKDIR /app

COPY ./app/ /app/
RUN chmod +x ./app.py
RUN useradd -m www
USER www
CMD /app/app.py