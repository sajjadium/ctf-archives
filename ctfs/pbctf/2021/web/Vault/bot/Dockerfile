FROM ubuntu:focal-20210723

RUN apt update && \
      apt install -y curl && \
      curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
      curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
      echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
      apt update && \
      DEBIAN_FRONTEND=noninteractive  apt install -y nodejs tightvncserver google-chrome-unstable && \
      rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash user

RUN cd /home/user && PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true npm install puppeteer

COPY bot.js /home/user/

USER user
WORKDIR /home/user

RUN mkdir -p /home/user/.vnc/ && echo -n 12345678 | vncpasswd -f > /home/user/.vnc/passwd && chmod 600 /home/user/.vnc/passwd

CMD USER=user vncserver :10 && DISPLAY=:10 PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome /usr/bin/node /home/user/bot.js