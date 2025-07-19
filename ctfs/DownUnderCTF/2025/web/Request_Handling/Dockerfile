FROM alpine:latest AS flag-builder

WORKDIR /build
RUN apk add gcc musl-dev
RUN cat <<EOF > getflag.c
#include <stdio.h>
int main() {
    printf("DUCTF{test_flag}\n");
}
EOF
RUN gcc -static getflag.c -o getflag

FROM node:22-alpine

WORKDIR /app
RUN npm init -y && npm install express@4 handlebars

RUN cat <<EOF > app.js
const express = require("express");
const Handlebars = require("handlebars");
const app = express();

app.get('/', (req, res) => {
    res.send(Handlebars.compile(req.query.x)({}));
});

app.listen(8000, () => console.log('App listening'));
EOF

COPY --from=flag-builder /build/getflag /getflag
RUN chmod 111 /getflag

EXPOSE 8000

USER node
CMD node app.js
