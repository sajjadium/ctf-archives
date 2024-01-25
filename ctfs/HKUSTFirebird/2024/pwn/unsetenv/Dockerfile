FROM ubuntu@sha256:145bacc9db29ff9c9c021284e5b7b22f1193fc38556c578250c926cf3c883a13

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y socat && rm -r /var/lib/apt/lists/*

WORKDIR /app
ADD unsetenv .
ADD spawn .
ADD flag.txt .
RUN chmod -R 755 /app && chmod 000 /app/flag.txt && chmod u+s /app/spawn

RUN for s in $(tail -n +2 /etc/shells); do rm -f $s; done

USER ubuntu

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:/app/spawn"]
