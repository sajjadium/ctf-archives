FROM node:12.18.1
WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install
ENV FLAG SOLVE_MY_CHALL
ENV PORT 3000
COPY . .
CMD ["npm", "start"]
