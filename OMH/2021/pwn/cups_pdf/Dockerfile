FROM ubuntu AS builder

RUN apt-get update -y && apt-get -y install gcc
ADD get_flag.c /
RUN gcc /get_flag.c -o /get_flag

FROM ubuntu

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN apt-get update -y && apt-get -y install cups-pdf

ADD cupsd.conf    /etc/cups/cupsd.conf
ADD printers.conf /etc/cups/printers.conf

COPY --from=builder /get_flag /get_flag
RUN chmod u=srx,go=x /get_flag

ADD flag /flag
RUN chmod u=r,go= /flag

EXPOSE 631/tcp
CMD ["/usr/sbin/cupsd"]
