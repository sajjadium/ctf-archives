FROM python:3.9
RUN apt update && apt upgrade -y
#RUN apt install -y ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libu2f-udev libvulkan1 lsb-release xdg-utils wget curl gnupg default-mysql-client git cron

RUN apt install -y cron

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY transfers /etc/cron.d/

RUN chmod 644 /etc/cron.d/transfers

ENTRYPOINT /etc/init.d/cron restart && python /app/app.py
