FROM mhart/alpine-node:16

WORKDIR /opt/app
COPY . .

RUN npm install
ENV NODE_ENV=production
ENV FLAG=buckeye{this_is_a_fake_flag}
CMD ["node", "app.js"]
