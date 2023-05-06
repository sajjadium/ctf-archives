# docker build -t unsafe . && docker run -p 4444:4444 --rm -it unsafe
 
 FROM ubuntu:21.04

 RUN apt update
 RUN apt install socat -y
 RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
 RUN echo "ctf:ctf" | chpasswd

 WORKDIR /home/ctf

 COPY flag .
 COPY unsafe .

 RUN chmod +x ./unsafe
 RUN chown root:root /home/ctf/unsafe
 RUN chown root:root /home/ctf/flag

 USER ctf

 CMD socat tcp-listen:4444,reuseaddr,fork exec:./unsafe,rawer,pty,echo=0

