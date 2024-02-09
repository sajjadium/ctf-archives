FROM alpine:latest@sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48
ENV PAGER=''
ENV FLAG='0xL4ugh{F4k3_Fl4G_F0r_T4stIng}'
RUN apk add socat python3 py3-pip
RUN adduser -D challenger
RUN pip3 install rich  --break-system-packages
WORKDIR /home/challenger
USER challenger
COPY challenge.py .
COPY exec.sh . 
ENTRYPOINT ["sh","exec.sh"]
