FROM python:3.9.0

LABEL maintainer "t0rchwo0d_LINE"

ENV SALT="ONLY_FOR_LOCAL_TEST"
ENV MEMO /usr/local/opt/memo-drive
RUN mkdir -p "${MEMO}"

RUN apt-get -qq update && \
  apt-get -qq -y upgrade && \
  apt-get -qq -y install htop net-tools vim

COPY ./memo-drive "${MEMO}"

COPY start.sh "${MEMO}/start.sh"
COPY flag "${MEMO}/memo/flag"

RUN pip install -r "${MEMO}/requirements.txt"

RUN chmod -R 705 "${MEMO}"
RUN chmod 707 "${MEMO}/memo/"
RUN chmod 704 "${MEMO}/memo/flag"

RUN groupadd -g 1000 memo
RUN useradd -g memo -s /bin/bash memo

USER memo
EXPOSE 11000
WORKDIR "${MEMO}"
ENTRYPOINT ["./start.sh"]
