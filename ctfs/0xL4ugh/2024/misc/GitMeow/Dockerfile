FROM alpine:latest@sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48
ENV PAGER=''
RUN apk add git
RUN apk add python3
COPY challenge.py /
COPY flag.txt /
COPY welcome.sh /
RUN chmod +x /welcome.sh
RUN ln /flag.txt /tmp/flag.txt  # In challenge Server flag file is named randomly 
RUN adduser -D challenger
WORKDIR /home/challenger
USER challenger
ENTRYPOINT ["sh","/welcome.sh"]