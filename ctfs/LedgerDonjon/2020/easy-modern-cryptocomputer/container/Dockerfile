# Setup a container with a node for Authenticated EOS.io blockchain.
#
# Usage:
#
#     podman build -t ctf-eosio .
#     podman run --rm -p 30510 -ti ctf-eosio start_nodeos
#
# Or with the provided saved Docker image:
#
#     wget https://cdn.donjon-ctf.io/modern_cryptocomputer_docker_save.bz2
#     echo '67b40e3370e83b8e955abb6bda826fc405f2db283b584753224e6a2bc968823c  modern_cryptocomputer_docker_save.bz2' |sha256sum -c
#     podman load -i modern_cryptocomputer_docker_save.bz2
#     podman run --rm -p 30510 -ti ctf-eosio start_nodeos

FROM ubuntu:18.04
LABEL Description="Modern Cryptocomputer"

# Patch from:
#   git -C eos --no-pager -c color.diff=never diff 'v2.0.7..HEAD' > eos_patch.patch
COPY blockchain.tar.bz2 eos_patch.patch start_genesis_nodeos start_nodeos /

# * Install dependencies from https://github.com/EOSIO/eos/blob/v2.0.7/docs/00_install/01_build-from-source/02_manual-build/03_platforms/ubuntu-18.04.md
# * Build and install EOSIO
# * Install EOSIO CDT (Contract Development Toolkit) using its Ubuntu package
# * Build the base EOSIO contracts, as documented in https://developers.eos.io/welcome/latest/tutorials/bios-boot-sequence/#18-build-eosiocontracts
# * Setup helper scripts and base blockchain data
RUN \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -qq update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
        autoconf \
        automake \
        autotools-dev \
        build-essential \
        bzip2 \
        ca-certificates \
        clang \
        clang-7 \
        cmake \
        curl \
        doxygen \
        git \
        graphviz \
        jq \
        libbz2-dev \
        libcurl4-gnutls-dev \
        libgmp3-dev \
        libicu-dev \
        libssl-dev \
        libtool \
        libusb-1.0-0-dev \
        llvm-7-dev \
        make \
        patch \
        pkg-config \
        python2.7 \
        python2.7-dev \
        python3 \
        python3-dev \
        ruby \
        sudo \
        vim-common \
        wget \
        zlib1g-dev \
    && \
    apt-get clean && \
    mkdir /opt/eosio && \
    git clone --no-checkout --single-branch --depth=1 --branch v2.0.7 https://github.com/EOSIO/eos /opt/eosio/eos && \
    git -C /opt/eosio/eos checkout v2.0.7 -b v2.0.7 && \
    git -C /opt/eosio/eos submodule update --init --recursive && \
    (cd /opt/eosio/eos && patch -p1 -i /eos_patch.patch) && \
    JOBS=4 /opt/eosio/eos/scripts/eosio_build.sh -i /opt/installdir && \
    JOBS=4 /opt/eosio/eos/scripts/eosio_install.sh && \
    wget -O /opt/eosio/eosio.cdt.deb https://github.com/eosio/eosio.cdt/releases/download/v1.7.0/eosio.cdt_1.7.0-1-ubuntu-18.04_amd64.deb && \
    apt-get install --no-install-recommends --no-install-suggests -y /opt/eosio/eosio.cdt.deb && \
    git clone --no-checkout --single-branch --depth=1 --branch v1.9.1 https://github.com/EOSIO/eosio.contracts /opt/eosio/eosio.contracts && \
    git -C /opt/eosio/eosio.contracts checkout v1.9.1 -b v1.9.1 && \
    (cd /opt/eosio/eosio.contracts && JOBS=4 ./build.sh -c /usr/bin) && \
    cp /start_genesis_nodeos /start_nodeos /opt/installdir/bin/ && \
    chmod +x /opt/installdir/bin/start_nodeos /opt/installdir/bin/start_genesis_nodeos && \
    rm -rf /opt/eosio/eos && \
    rm /opt/eosio/eosio.cdt.deb && \
    rm -rf /opt/installdir/src/ && \
    rm -rf /var/lib/apt/lists/*

# Expose ports 30510 ("EOSIO") for HTTP endpoint and 9010 for EOS p2p endpoint
EXPOSE 30510/tcp 9010/tcp

# Add EOSIO binaries to $PATH and define default keys (that can be overridden with "podman run -e ...")
# By default, the keys are the "development keys" documented on https://developers.eos.io/welcome/latest/getting-started/development-environment/create-development-wallet/
# In order to create your own keys, run:
#
#    cleos create key --to-console
#
# You may import the key in a wallet using: cleos wallet import --private-key
ENV PATH="/opt/installdir/bin:${PATH}" \
    EOS_NODE_PRIV_KEY=5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3 \
    EOS_NODE_PUB_KEY=EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV \
    EOS_GENESIS_INITIAL_KEY=EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV \
    FLAG=This_is_not_the_flag_you_are_looking_for

WORKDIR "/opt/eosio"
CMD [ "/opt/installdir/bin/start_nodeos" ]
