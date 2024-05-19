FROM registry.fedoraproject.org/fedora@sha256:0736bade1cf7edf5eb1603b44426d388bdb2d2de93759a9a1c856211b0539246

RUN /usr/sbin/useradd -u 1000 user

RUN dnf install ca-certificates socat libseccomp-devel -y

WORKDIR /home/user/
COPY flag challenge_bin /home/user/

RUN chown root:root flag challenge_bin 
RUN chmod 444 flag challenge_bin
RUN chown user:user /home/user
RUN chmod 755 /home/user
RUN setcap cap_sys_chroot+eip challenge_bin

RUN chmod a+x /home/user/challenge_bin

EXPOSE 1339

USER user
CMD   socat \
      TCP-LISTEN:1339,reuseaddr,fork \
      EXEC:"timeout 120 /home/user/challenge_bin"