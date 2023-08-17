FROM archlinux:latest

# Note to self: Use docker-compose, you fucking idiot.

# install packages
RUN pacman-key --init && pacman --noconfirm -Sy archlinux-keyring && pacman -Syu --noconfirm firefox python python-pip

# install python-selenium
RUN pip install requests argparse --break-system-packages

COPY watcher.py /
CMD bash -c 'python /watcher.py -l 0.0.0.0'