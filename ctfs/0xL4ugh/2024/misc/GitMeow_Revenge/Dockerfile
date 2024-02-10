FROM alpine:latest@sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48
WORKDIR /home/challenger
ENV PAGER=''
RUN apk add git python3 socat
COPY challenge.py .
COPY banner.py .
COPY flag.txt /
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
RUN ln /flag.txt /tmp/flag.txt  # In challenge Server flag file is named randomly 
RUN adduser -D challenger
USER challenger
ENTRYPOINT ["sh","entrypoint.sh"]