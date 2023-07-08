FROM sagemath/sagemath:latest

RUN sudo apt-get update && sudo apt-get install -y tzdata  # avoid select timezone
RUN sudo apt-get update && sudo apt-get upgrade -y
RUN sudo apt-get update && sudo apt-get install socat -y

### diretory setting
COPY --chown=sage:sage server.sage /home/sage/server.sage
COPY --chown=sage:sage secret.py /home/sage/secret.py
COPY --chown=sage:sage flag.py /home/sage/flag.py

USER sage

RUN sage --pip install pycryptodome

ENV PYTHONUNBUFFERED=1

RUN sage --python /home/sage/secret.py

EXPOSE 5000

CMD ["/usr/bin/socat", "tcp-listen:5000,reuseaddr,fork", "exec:\"/home/sage/sage/sage server.sage\""]
