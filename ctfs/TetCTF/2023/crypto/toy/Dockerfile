FROM continuumio/miniconda3

RUN conda config --add channels conda-forge
RUN conda install socat
RUN conda install pycryptodome

RUN useradd toy -m
COPY . /home/toy

USER toy:toy
WORKDIR /home/toy

CMD socat -T 30 -d -d TCP-LISTEN:31337,reuseaddr,fork EXEC:"python -u toy.py"