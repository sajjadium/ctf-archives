FROM redpwn/jail:0.1.3

# ubuntu:focal-20220404
COPY --from=ubuntu@sha256:31cd7bbfd36421dfd338bceb36d803b3663c1bfa87dfe6af7ba764b5bf34de05 / /srv

# create bin/flag.txt with whatever inside
COPY bin/flag.txt /srv/app/
COPY bin/chall /srv/app/run
