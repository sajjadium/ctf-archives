FROM archlinux:20200908

RUN pacman --noconfirm -Sy xinetd

# ctf user
RUN useradd -m -s /bin/bash ctf

# challenge files
COPY howtoheap /home/ctf/
COPY flag.txt /home/ctf/
COPY howtoheap_svc /etc/xinetd.d/

CMD xinetd -dontfork
