FROM gcr.io/paradigmxyz/ctf/eth-challenge:latest as chroot

USER root

ENV HUFF_DIR=/opt/huff

ENV PATH=${HUFF_DIR}/bin/:${PATH}

RUN true && \
    curl -L http://get.huff.sh | bash && \
    huffup && \
    true

USER user

COPY --chown=user:user project/ /home/user/project/

RUN cd /home/user/project && forge build && sed -i 's@binary_check();@// REMOVED@g' lib/foundry-huff/src/HuffConfig.sol

COPY --chown=user:user *.py /home/user/

FROM gcr.io/paradigmxyz/ctf/kctf-challenge:latest

VOLUME [ "/chroot", "/tmp" ]

COPY --from=chroot / /chroot

# nsjail help
RUN touch /chroot/bin/kctf_restore_env && touch /chroot/environ

CMD kctf_setup && \
    kctf_persist_env && \
    kctf_drop_privs nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /usr/local/bin/python3 -u -m anvil_server & \
    kctf_drop_privs socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"nsjail --config /nsjail.cfg -- /bin/kctf_restore_env /usr/local/bin/python3 -u challenge.py"
