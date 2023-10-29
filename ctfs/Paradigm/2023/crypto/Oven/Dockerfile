FROM python:3.11.6-slim as chroot

# Set up unprivileged user and install dependencies
RUN true && \
  useradd -u 1000 -m user && \
  apt-get update && \
  apt-get install -y build-essential && \
  rm -rf /var/cache/apt/lists /var/lib/apt/lists/* && \
  true

USER user
WORKDIR /home/user

COPY --chown=user:user *.py requirements.txt /home/user/

RUN true && \
  pip install -r requirements.txt && \
  true

FROM gcr.io/paradigmxyz/ctf/kctf-challenge:latest

VOLUME [ "/chroot", "/tmp" ]

COPY --from=chroot / /chroot

# nsjail help
RUN touch /chroot/bin/kctf_restore_env && touch /chroot/environ

CMD kctf_setup && \
  kctf_persist_env && \
  kctf_drop_privs socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /usr/local/bin/python3 -u challenge.py"
