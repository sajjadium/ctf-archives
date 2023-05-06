FROM node

RUN apt update && apt dist-upgrade -y && \
	apt install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get -y install google-chrome-stable libxss1


RUN git clone https://github.com/GoogleChrome/rendertron.git && cd rendertron && npm install && npm run build
WORKDIR /rendertron
CMD ["npm","run","start"]
