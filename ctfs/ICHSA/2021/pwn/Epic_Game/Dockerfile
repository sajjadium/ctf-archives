FROM gcc:10-buster as build

RUN mkdir -p /app
COPY epic_game.c epic_game.h /app

WORKDIR /app

RUN gcc epic_game.c -fstack-protector -fpie -fPIE -fpic -o app.out

FROM debian:buster-slim as app

WORKDIR /app
COPY flag.txt /app/	
RUN chmod 0444 /app/flag.txt

COPY --from=build /app/app.out /app/app.out

RUN apt-get update && apt-get install -y socat

# Set non root user
RUN useradd -c 'User' -m -d /home/user -s /bin/bash user
RUN chown -R user:user /home/user

USER user
ENV HOME /home/user

EXPOSE 8007
CMD ["socat", "-dd", "-T60", "TCP4-LISTEN:8007,fork,reuseaddr", "EXEC:/app/app.out,pty,setuid=user,echo=0,raw,iexten=0"]