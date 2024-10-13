FROM thekidofarcrania/chall31

ENV LIBC_HASH 59e53203baf0667facd95946d27239694359e09e0cd71aa11355918cdfd7b2ae
ENV LIBC_FILE /lib/x86_64-linux-gnu/libc.so.6

RUN mkdir /app && \
  echo "$LIBC_HASH $LIBC_FILE" | sha256sum -c && \
  /bin/echo -ne '\x07' | dd of=$LIBC_FILE seek=629249 bs=1 conv=notrunc

COPY todo.conf /etc/xinetd.d/todo
COPY todo /app
COPY flag.txt /

EXPOSE 1337

CMD ["xinetd", "-dontfork"]
