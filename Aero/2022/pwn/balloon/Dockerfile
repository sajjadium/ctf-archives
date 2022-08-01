FROM python:3.11-rc-slim AS builder

RUN for name in 'ctypes' 'pickle' 'test' 'cffi'; do \
        find /usr/local/lib/python3.11/ -name "*${name}*" -exec rm -rf '{}' '+'; \
    done

FROM alpine:3.16.1

RUN apk add coreutils

COPY --from=builder /lib/x86_64-linux-gnu /chroot/lib/x86_64-linux-gnu
COPY --from=builder /lib64/ld-linux-x86-64.so.2 /chroot/lib64/ld-linux-x86-64.so.2
COPY --from=builder /usr/lib/x86_64-linux-gnu /chroot/usr/lib/x86_64-linux-gnu
COPY --from=builder /usr/local/lib/python3.11 /chroot/usr/local/lib/python3.11
COPY --from=builder /usr/local/lib/libpython3.11.so.1.0 /chroot/usr/lib/libpython3.11.so.1.0

COPY --from=builder /usr/local/bin/python3.11 /chroot/bin/

COPY preload.so balloon.py flag /chroot/challenge/

RUN chmod 111 /chroot/challenge/flag \
    && chmod 555 /chroot/challenge/preload.so \
    && chmod 444 /chroot/challenge/balloon.py

COPY entrypoint.sh /tmp/entrypoint.sh

RUN chmod 555 /tmp/entrypoint.sh

ENTRYPOINT [ "/tmp/entrypoint.sh" ]
