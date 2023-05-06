# build your debug container with docker build -t hacklu:leaky .
# start your debug container with docker run -it hacklu:leaky

FROM ubuntu:22.04
ENV user ctf

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3

RUN useradd ${user} -m -s /bin/bash
WORKDIR /chal
COPY main /chal/sigs
ADD flag /flag
RUN chown root /flag
RUN chmod 400 /flag
RUN chown root /chal/sigs
RUN chmod u+s /chal/sigs

USER ${user}
CMD ["/bin/bash"]
