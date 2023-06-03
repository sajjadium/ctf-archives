FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

##################################### NSJAIL SETUP #####################################
RUN apt update && apt install -y curl wget xz-utils sudo coreutils

# Install Nix package manager
# (We could do it with sh curl, but we better validate the .tar.xz with a hash)
#RUN bash -c "sh <(curl -L https://nixos.org/nix/install) --no-daemon"
RUN wget https://releases.nixos.org/nix/nix-2.15.1/nix-2.15.1-x86_64-linux.tar.xz && \
    tar -xvf nix-2.15.1-x86_64-linux.tar.xz && \
    echo '9345c1485dadb1cb66ed54aa97c692ab38f7ead2d609230564e6673490f30365 nix-2.15.1-x86_64-linux.tar.xz' | sha256sum -c

RUN adduser --disabled-password --gecos '' nix && \
    adduser nix sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER nix
ENV USER=nix
RUN cd nix-2.15.1-x86_64-linux && \
    ./install --no-daemon

# Install Nsjail using Nix
RUN . /home/nix/.nix-profile/etc/profile.d/nix.sh && \
    nix-env -iA nixpkgs.nsjail

# Bring back root user
USER root
ENV USER=root

# Eventually, disable sudo
RUN sed -i '$ d' /etc/sudoers 
############################# END OF NSJAIL SETUP #####################################

# install task dependencies
RUN adduser --gecos '' jailed
RUN mkdir /jailed/
WORKDIR /jailed
ENV HOME=/jailed

# rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/jailed/.cargo/bin:${PATH}"
RUN sudo apt install -y build-essential

# python
RUN sudo apt install -y python3 python3-pip

# nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
    sudo apt install -y nodejs

# golang
RUN wget https://go.dev/dl/go1.20.4.linux-amd64.tar.gz && sudo tar -C /usr/local -xzf go1.20.4.linux-amd64.tar.gz && rm go1.20.4.linux-amd64.tar.gz
ENV PATH="$PATH:/usr/local/go/bin"

COPY ./src/ .
RUN chown -R jailed:jailed /jailed/
USER jailed
RUN cargo install --path ./dispatcher/
RUN go build -o indexgo ./index.go

COPY ./nsjail.cfg /nsjail.cfg
USER root
ENV USER=root
CMD ["/home/nix/.nix-profile/bin/nsjail", "--config", "/nsjail.cfg"]
