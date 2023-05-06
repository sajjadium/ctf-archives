FROM ubuntu:18.04
RUN apt update && apt upgrade -y && apt install -y git build-essential python
RUN git clone https://github.com/ocaml/ocaml /ocaml
WORKDIR /ocaml
RUN git checkout a095535e5c02a95da4908a82d9f75a62609cc592 && ./configure
RUN make world.opt && make install

RUN apt install -y python3.7
RUN groupadd -r user && useradd -m -r -g user user
COPY --chown=root:user ./env /env
COPY --chown=root:user ./flag /flag
RUN chmod 444 /flag

USER user
WORKDIR /env
ENV PYTHONUNBUFFERED=x
CMD ["./run.py"]
