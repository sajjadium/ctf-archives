
FROM fedora:33

RUN dnf update -y && dnf install -y xinetd

# challenge user and home 
ENV CHALL_USER=ctf
ENV CHALL_PATH=/home/$CHALL_USER
RUN useradd -m $CHALL_USER

WORKDIR $CHALL_PATH

# chall files and flag
COPY dist/* ./
RUN chown -R root:$CHALL_USER $(pwd) && \
    chmod -R 650 $(pwd)

RUN cp ./libasmjit.so /usr/lib64 && \
    chown root:root /usr/lib64/libasmjit.so && \
    chmod -R 655 /usr/lib64/libasmjit.so

COPY flags ./flags
RUN chown -R root:$CHALL_USER ./flags && \
    chmod -R 640 ./flags

# prepare xinetd
COPY ./conf/chall.xinetd /etc/xinetd.d/chall
COPY ./conf/start.sh /start.sh
RUN echo "Blocked by xinetd" > /etc/banner_fail && chmod +x /start.sh

EXPOSE 2000
CMD ["/start.sh"]
