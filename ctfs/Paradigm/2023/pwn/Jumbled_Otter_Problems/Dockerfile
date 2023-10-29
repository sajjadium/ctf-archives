FROM rust:1.70.0 AS chroot

ENV PATH="/home/user/.local/share/solana/install/active_release/bin:${PATH}"

RUN true && \
    useradd -u 1000 -m user && \
    apt-get update && \
    apt-get install -y libudev-dev && \
    rm -rf /var/cache/apt/lists /var/lib/apt/lists/* && \
    true

USER user
WORKDIR /home/user

RUN true && \
    curl -L https://release.solana.com/v1.17.3/install | bash && \
    true

COPY --chown=user:user framework /home/user/framework

RUN true && \
    cd /home/user/framework/chall && \
    cargo build-sbf && \
    cd /home/user/framework && \
    cargo build --release && \
    true

FROM ubuntu:20.04 AS intermediate

RUN true && \
    useradd -u 1000 -m user && \
    true

USER user
WORKDIR /home/user

COPY --chown=user:user framework /home/user/framework

COPY --from=chroot /home/user/framework/chall/target/deploy/chall.so /home/user/framework/chall.so
COPY --from=chroot /home/user/framework/target/release/framework /home/user/framework/bin

FROM gcr.io/paradigmxyz/ctf/kctf-challenge:latest

VOLUME [ "/chroot", "/tmp" ]

COPY --from=intermediate / /chroot

# nsjail help
RUN touch /chroot/bin/kctf_restore_env && touch /chroot/environ

CMD kctf_setup && \
    kctf_persist_env && \
    kctf_drop_privs nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /home/user/framework/bin
