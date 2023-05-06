FROM node:16-alpine
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
RUN chown nextjs:nodejs /app 

COPY --chown=nextjs:nodejs ./next.config.js ./
COPY --chown=nextjs:nodejs ./package.json ./
COPY --chown=nextjs:nodejs ./package-lock.json ./
COPY --chown=nextjs:nodejs ./pages ./pages
COPY --chown=nextjs:nodejs ./public ./public
COPY --chown=nextjs:nodejs ./styles ./styles
COPY --chown=nextjs:nodejs ./utils ./utils

USER nextjs

EXPOSE 3000

RUN npm install
RUN npm run build

CMD ["npm", "start"]
