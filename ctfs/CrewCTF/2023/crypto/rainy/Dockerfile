FROM sagemath/sagemath:latest

RUN sudo apt-get update && sudo apt-get install -y tzdata  # avoid select timezone
RUN sudo apt-get update && sudo apt-get upgrade -y
RUN sudo apt-get update && sudo apt-get install socat -y

### diretory setting
COPY --chown=sage:sage common.sage /home/sage/common.sage
COPY --chown=sage:sage keygen.sage /home/sage/keygen.sage
COPY --chown=sage:sage server.sage /home/sage/server.sage
COPY --chown=sage:sage flag.py /home/sage/flag.py

USER sage

RUN /home/sage/sage/sage keygen.sage
EXPOSE 1337

CMD ["/usr/bin/socat", "tcp-listen:1337,reuseaddr,fork", "exec:\"/home/sage/sage/sage server.sage\""]
