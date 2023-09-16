FROM denoland/deno:1.36.4
WORKDIR /app

RUN apt-get update && apt-get install -yq socat procps

COPY flag.txt .
RUN mv flag.txt /flag-$(md5sum flag.txt | cut -c-32).txt

COPY index.ts .

USER deno

CMD socat -T30 tcp-listen:1337,fork,reuseaddr exec:"deno run --allow-read --no-prompt index.ts",pty,raw,echo=0
