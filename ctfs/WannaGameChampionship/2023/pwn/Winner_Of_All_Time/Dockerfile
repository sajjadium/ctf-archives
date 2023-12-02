FROM ubuntu:23.04

RUN apt-get update ; \
 apt-get install -y socat
WORKDIR /app

COPY winner_of_all_time flag /app/

RUN chmod +x /app/winner_of_all_time && \
    useradd -m nonroot && \
    chown -R nonroot:nonroot /app

USER nonroot

CMD socat \
       TCP-LISTEN:13337,reuseaddr,fork \
       EXEC:"/app/winner_of_all_time"
