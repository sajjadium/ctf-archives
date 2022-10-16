FROM ubuntu:22.04

COPY ./stuff/readme /home/pwn/readme
COPY ./stuff/run /home/pwn/run
RUN chown -R root /home/pwn/*   
RUN chmod +x /home/pwn/run; 
RUN chmod 111 /home/pwn/readme;
RUN chmod u+s /home/pwn/readme;
RUN useradd pwn;
CMD ["/home/pwn/run"];