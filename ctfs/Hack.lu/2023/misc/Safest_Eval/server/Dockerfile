FROM alpine AS compiler

RUN apk add --no-cache gcc musl-dev
COPY ./readflag.c /readflag.c
RUN gcc -o /readflag /readflag.c

FROM python:3.11-alpine

RUN apk add --no-cache iptables sudo
COPY --from=compiler /readflag /readflag
COPY ./flag /flag
RUN mkdir -p /app && adduser -D safe_eval && chmod 400 /flag && chmod 4555 /readflag
WORKDIR /app/
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ /app/
RUN chmod +x /app/entrypoint.sh

CMD /app/entrypoint.sh