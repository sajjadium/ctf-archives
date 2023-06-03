FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 

##################################### NSJAIL SETUP #####################################
RUN apt update && apt install -y curl xz-utils sudo coreutils wget

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

RUN mkdir /jailed

# We build sqlite3 from scratch with no modifications. Let's not do it again
# and just copy the pre-build binary (We did zero modifications to sqlite3 sources)
# MD5 (sqlite3) = 9177aaa0ffe4a692f4663835d8bab5f2
#WORKDIR /tmp
#RUN apt update && apt install gcc build-essential wget make tcl libssl-dev zlib1g-dev -yy
#RUN wget https://github.com/sqlite/sqlite/archive/refs/tags/version-3.42.0.tar.gz
#RUN tar xf version-3.42.0.tar.gz
#RUN cd sqlite-version-3.42.0 && mkdir build && cd build && ../configure && make && cp sqlite3 /jailed
COPY ./sqlite3 /jailed/sqlite3

WORKDIR /jailed

RUN adduser --gecos '' jailed
RUN adduser --gecos '' flagreader
RUN chown -R jailed:jailed /jailed

COPY flag.txt .
RUN chmod 400 flag.txt
COPY readflag .
RUN chown flagreader:flagreader readflag flag.txt && chmod 4755 readflag

COPY run-sqlite.sh .

CMD ["/home/nix/.nix-profile/bin/nsjail", "--config", "/nsjail.cfg"]
