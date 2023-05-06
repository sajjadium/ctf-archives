FROM node:12.18.1

RUN apt-get update


#INSTALL CHROME
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update -y
RUN apt-get install google-chrome-stable -yqq

WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install
ENV FLAG FLAGNOTVALID{Solve_My_Challenge}
COPY . .
CMD ["npm", "start"]
