ARG IMAGE
FROM $IMAGE

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y > /dev/null
RUN apt-get upgrade -y > /dev/null
RUN apt-get install xinetd -y > /dev/null

ARG USER
ARG TIMEOUT
ARG EXEC
RUN useradd -ms /bin/bash $USER
ADD ./share /home/$USER
RUN echo "#!/bin/bash\ntimeout $TIMEOUT /home/$USER/$EXEC" \
        > /home/$USER/run.sh
RUN chown -R root:$USER /home/$USER
RUN chmod -R 750 /home/$USER

ARG SERVICE
RUN echo "service $SERVICE\n{\n\tdisable = no\n\tflags = REUSE\n\tsocket_type = stream\n\tprotocol = tcp\n\tuser = $USER\n\twait = no\n\tserver = /home/$USER/run.sh\n\ttype = UNLISTED\n\tport = 45510\n}" \
        > /etc/xinetd.d/$SERVICE
CMD ["/usr/sbin/xinetd", "-dontfork"]