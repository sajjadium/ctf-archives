FROM ubuntu:22.04@sha256:ec050c32e4a6085b423d36ecd025c0d3ff00c38ab93a3d71a460ff1c44fa6d77

ENV user ctf
ENV port 4444
ENV flag flag.txt
ENV chal dumb_contract

# Install packages
RUN apt-get update
RUN apt-get install -y socat

# Change permission
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Copy binaries and flag
RUN adduser $user
ADD ./$chal /home/$user/$chal
ADD ./$flag /home/$user/$flag
RUN chown -R root:$user /home/$user/
RUN chown root:$user /home/$user/$chal
RUN chown root:$user /home/$user/$flag
RUN chmod 2755 /home/$user/$chal
RUN chmod 440 /home/$user/$flag

# final
CMD socat -T 5 TCP-LISTEN:$port,reuseaddr,fork EXEC:/home/$user/$chal
USER $user
EXPOSE $port