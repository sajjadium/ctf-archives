FROM rust:1.73-buster AS foundry-builder

COPY patches /workdir/patches

RUN true && \
    apt-get update && \
    apt-get install -y clang && \
    cd /workdir && \
    git clone https://github.com/foundry-rs/foundry.git && \
    (cd foundry && git checkout nightly-619f3c56302b5a665164002cb98263cd9812e4d5 && git apply ../patches/foundry.patch) && \
    git clone https://github.com/bluealloy/revm.git && \
    (cd revm && git checkout v26 && git apply ../patches/revm.patch) && \
    true

RUN true && \
    cd /workdir/foundry && \
    cargo build -p anvil && \
    true

FROM gcr.io/paradigmxyz/ctf/eth-challenge:latest as chroot

COPY --from=foundry-builder /workdir/foundry/target/debug/anvil /opt/foundry/bin/anvil-l2

COPY --chown=user:user project /home/user/project

RUN cd /home/user/project && forge build

COPY --chown=user:user *.py /home/user/

FROM gcr.io/paradigmxyz/ctf/kctf-challenge:latest

VOLUME [ "/chroot", "/tmp" ]

COPY --from=chroot / /chroot

# nsjail help
RUN touch /chroot/bin/kctf_restore_env && touch /chroot/environ

CMD kctf_setup && \
    kctf_persist_env && \
    kctf_drop_privs nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /usr/local/bin/python3 -u -m anvil_server & \
    kctf_drop_privs socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /usr/local/bin/python3 challenge.py"
