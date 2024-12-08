# syntax=docker/dockerfile:latest

#FROM docker.io/library/ubuntu@sha256:562456a05a0dbd62a671c1854868862a4687bf979a96d48ae8e766642cd911e8 as base

## Enable APT package caching
#RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    #echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

## Install packages
#RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    #--mount=type=cache,target=/var/lib/apt,sharing=locked \
    #apt-get update && \
    #apt-get install -y --no-install-recommends qemu-system-x86-64 socat
#RUN useradd -u 1000 jail || true


#FROM pwn.red/jail

#COPY --from=base / /srv
#COPY --chmod=0777 ZealOS.qcow2 /srv/app/
#COPY --chmod=0755 run_qemu.sh /srv/app/
#COPY --chmod=0777 run_jail.sh /srv/app/run
#COPY --chmod=0777 hook.sh /jail/hook.sh

#ENV JAIL_TIME 120
#ENV JAIL_PIDS 500
#ENV JAIL_CPU 2000
#ENV JAIL_CONNS_PER_IP 5
#ENV JAIL_MEM 10G
#ENV JAIL_TMP_SIZE 2000M
#ENV JAIL_DEV null,zero,urandom,kvm





FROM docker.io/library/ubuntu@sha256:562456a05a0dbd62a671c1854868862a4687bf979a96d48ae8e766642cd911e8 as base

# Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
	echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Install packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
	--mount=type=cache,target=/var/lib/apt,sharing=locked \
	apt-get update && \
	apt-get install -y --no-install-recommends qemu-system-x86-64 socat golang-go xz-utils

COPY --chmod=0777 ZealOS.qcow2.xz /
#COPY --chmod=0777 ZealOS_fake_flag.qcow2.xz /ZealOS.qcow2.xz
COPY --chmod=0777 ghetto_nsjail.sh /
COPY --chmod=0777 run_qemu.sh /
COPY --chmod=0777 pow/redpwnpow /
WORKDIR /

RUN xz -d /ZealOS.qcow2.xz 

CMD socat TCP-LISTEN:5000,fork,reuseaddr system:"/redpwnpow && /ghetto_nsjail.sh; echo 'Done'; exit"










