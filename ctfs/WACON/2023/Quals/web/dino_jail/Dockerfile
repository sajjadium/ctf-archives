FROM denoland/deno@sha256:b703c0e2f44c36fb00c11715f60bddcdddc465f22a9758b6e1430ec5584cc04b

RUN apt update
RUN apt install gcc -y

COPY ./jail.js /jail.js
COPY ./flag.txt /flag.txt
COPY ./readflag.c /tmp/readflag.c

RUN gcc -static -o /readflag /tmp/readflag.c
RUN rm /tmp/readflag.c

RUN chmod 444 /jail.js
RUN chmod 400 /flag.txt
RUN chown root /flag.txt /jail.js /readflag
RUN chmod u+s /readflag

ENTRYPOINT ["timeout","-s9","3","deno","run","--allow-write","--allow-read","--allow-ffi","--unstable","/jail.js"]
