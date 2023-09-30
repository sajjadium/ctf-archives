FROM sagemath/sagemath

USER root

WORKDIR /app

RUN apt-get update
RUN apt-get install -y socat git

# Many thanks to Maria Corte-Real Santos, Jonathan Komada Eriksen
# Michael Meyer and Giacomo Pope for this amazing repo!
RUN git clone https://github.com/LearningToSQI/SQISign-SageMath.git
COPY ./changes.patch ./SQISign-SageMath/

RUN (cd SQISign-SageMath; git apply changes.patch)

COPY ./public_key .
COPY ./check_signature.sage .

ENTRYPOINT ["socat", "-t", "900", "-T", "120", "TCP4-LISTEN:5555,reuseaddr,fork", "EXEC:env PYTHONUNBUFFERED=1 sage check_signature.sage"]