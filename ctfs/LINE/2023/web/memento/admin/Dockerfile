FROM node:18

RUN apt update
RUN apt-get install -y libnss3\
    libnspr4\                
    libatk1.0-0\             
    libatk-bridge2.0-0\      
    libcups2\                
    libdbus-1-3\             
    libatspi2.0-0\           
    libxcomposite1\          
    libxdamage1\             
    libxfixes3\              
    libxrandr2\              
    libgbm1\                 
    libdrm2\                 
    libxkbcommon0\           
    libasound2

WORKDIR /usr/src/app
RUN useradd -m -U user
COPY package*.json ./
RUN chown -R user:user /usr/src/app 
USER user

RUN npm i
RUN npx playwright install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]