from ubuntu:18.04

run groupadd -r ctf && useradd --no-log-init -r -g ctf ctf

run dpkg --add-architecture i386
run apt-get update && apt-get upgrade -y
run apt-get install -y socat libc6:i386 libncurses5:i386 libstdc++6:i386 python3

copy ./right_spot ./run.py ./run_socat.sh ./flag.py /chall/

WORKDIR /chall
run chmod +x right_spot run.py run_socat.sh

CMD /chall/run_socat.sh