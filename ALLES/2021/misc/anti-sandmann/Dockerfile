FROM alpine:latest as builder
WORKDIR /build
RUN apk add git gcc g++ make readline-dev
COPY cpython.patch /cpython.patch

RUN git init && git remote add origin https://github.com/python/cpython.git && git fetch --depth 1 origin db3ff76da19004f266b62e98a81bdfd322861436 && git checkout FETCH_HEAD && git apply ../cpython.patch
RUN ./configure --with-zlib && make -j12

WORKDIR /ynetd
COPY ynetd-0.1.2.tar.xz .
RUN tar -xf ynetd-0.1.2.tar.xz && cd ynetd-0.1.2 && make

FROM alpine:latest as runner
WORKDIR /
RUN apk add readline
COPY chall.py /chall.py
COPY --from=builder /build /build
COPY flag /flag
COPY --from=builder /ynetd/ynetd-0.1.2/ynetd /ynetd
EXPOSE 1024
CMD /ynetd -se y "/build/python /chall.py"
