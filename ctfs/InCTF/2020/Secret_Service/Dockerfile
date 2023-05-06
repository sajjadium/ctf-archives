FROM ubuntu:20.04

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN  apt-get update && \
     apt-get -y upgrade && \
     apt-get install -y libseccomp-dev && \
     apt-get install -y xinetd && \
     apt-get install -y gdb && \
     apt-get install -y git && \
     apt-get install -y gcc python2.7-dev && \
     apt-get install -y software-properties-common && \
     apt install -y python2 && \
     apt-get update && \
     apt install -y curl && \
     curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py && \
     python2 get-pip.py && \
     pip install --upgrade setuptools

RUN  python2.7 -m pip install --upgrade pwntools

RUN useradd -m ctf

WORKDIR /home/ctf

ADD chall /home/ctf
ADD libseccomp.so.2 /home/ctf
ADD exp.py /home/ctf
ADD libc.so.6 /home/ctf
RUN cp libseccomp.so.2 /usr/lib/x86_64-linux-gnu/
RUN git clone https://github.com/longld/peda.git ~/peda
RUN echo "source ~/peda/peda.py" >> ~/.gdbinit
RUN apt install -y vim 
RUN apt-get install -y tmux
