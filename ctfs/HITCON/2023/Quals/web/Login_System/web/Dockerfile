FROM nimlang/nim:1.6.14-alpine as builder

WORKDIR /tmp
RUN nimble install jester@0.6.0 -y
COPY ./src/login_sys.nim .
RUN nim c -d:release -d:useStdLib login_sys

FROM node:20-alpine

WORKDIR /app
COPY ./package.json .
RUN yarn
COPY ./src ./src
COPY --from=builder /tmp/login_sys .
# readflag is a precompiled binary that will print the flag when executed
COPY readflag /readflag
RUN chmod 111 /readflag && mkdir -p /users && chown -R nobody:nobody /users
ENV USER_DIR=/users
COPY ./run.sh .

USER nobody
CMD ["sh", "-c", "timeout $TIMEOUT /app/run.sh"]
