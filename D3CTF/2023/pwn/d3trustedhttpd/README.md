# d3TrustedHttpd

## Desc

Trust me or not, you will never be able to break it.

Address: `http://{ip}:{port}/`

## Run

1. Download and build QEMU 7.2.0:

    ```shell
    wget https://download.qemu.org/qemu-7.2.0.tar.xz
    tar xvJf qemu-7.2.0.tar.xz
    cd qemu-7.2.0
    ./configure --target-list=aarch64-softmmu --enable-slirp --disable-spice-protocol
    make -j `nproc`
    # make install
    ```

2. Run QEMU with `./run.sh`.

3. Access challenge from `http://localhost:8080`.

## Notice

1. Some of the sensitive data embedded in the firmware is different from the remote, so please check through the remote environment.

2. Please destroy and re-create a new environment at the competition platform, if the key service is abnormal.

3. Please do not launch any kind of DDoS attack except for the interaction needed to complete the challange.

4. If you have other questions please ask for help in the online group.

## Author

Eqqie @ D^3CTF
