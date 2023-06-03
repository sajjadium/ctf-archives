FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

##################################### NSJAIL SETUP #####################################
# We install nsjail from nix package manager that we first install
# that is just easier lol
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
COPY ./nsjail.cfg /nsjail.cfg

# Bring back root user
USER root
ENV USER=root

# Eventually, disable sudo
RUN sed -i '$ d' /etc/sudoers 
############################# END OF NSJAIL SETUP #####################################

# Challenge data/files
RUN adduser --gecos '' jailed
RUN adduser --gecos '' flagreader

RUN mkdir /jailed/

COPY ./binaries/readflag /jailed/readflag
COPY ./flag.txt /jailed/flag.txt

COPY ./binaries/rpc_server /jailed/rpc_server
COPY ./binaries/rpc_tictactoe.so /jailed/rpc_tictactoe.so

# Set permissions accordingly...
RUN chown -R jailed:jailed /jailed/
RUN chown flagreader:flagreader /jailed/readflag /jailed/flag.txt && \
    chmod 4755 /jailed/readflag && \
    chmod 400 /jailed/flag.txt

CMD ["/home/nix/.nix-profile/bin/nsjail", "--config", "/nsjail.cfg"]
