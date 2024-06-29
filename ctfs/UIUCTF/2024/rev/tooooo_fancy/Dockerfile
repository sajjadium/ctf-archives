FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /home/chal
RUN mkdir /home/chal/src

RUN apt-get update && apt-get install -y tclsh git wget gcc make vim

# Install active tcl
WORKDIR /home/chal
RUN git clone https://github.com/ActiveState/teapot.git --depth 1
RUN git clone https://github.com/cyangy/tdk.git --depth 1
RUN wget https://dl.activestate.com/pre-platform-installer/ActiveTcl-8.6.9.8609.2-x86_64-linux-glibc-2.5-dcd3ff05d.tar.gz
RUN tar -xf *.tar.gz && rm -rf *.tar.gz && mv ActiveTcl* ActiveTcl
WORKDIR /home/chal/ActiveTcl
RUN echo -e "\nA\n\n\n\n\n\n" | ./install.sh
RUN echo "TCL_SRC_DIR='/opt/ActiveTcl-8.6/include'" >> /opt/ActiveTcl-8.6/lib/tclConfig.sh

# Used to compile the program
WORKDIR /home/chal/tdk/lib/tclcompiler
RUN sed -i 's/generic\/tclInt/tclInt/g' ./configure
RUN ./configure --with-tcl=/opt/ActiveTcl-8.6/lib
RUN make

# Used to run the program
WORKDIR /home/chal/teapot/lib/tbcload
RUN sed -i 's/generic\/tclInt/tclInt/g' ./configure
RUN ./configure --with-tcl=/opt/ActiveTcl-8.6/lib
RUN make

WORKDIR /home/chal/src

# TO COMPILE, UNCOMMENT OUT THIS SECTION
# COPY main.tcl /home/chal/src/main.tcl
# RUN echo "package ifneeded compiler 1.7.1 [list load [file join /home/chal/tdk/lib/tclcompiler libtclcompiler1.7.1.so]];\npackage require compiler;\ncompiler::compile main.tcl main.tbc" >> compiler.tcl
# RUN tclsh compiler.tcl
# RUN (echo "package ifneeded tbcload 1.7 [list load [file join /home/chal/teapot/lib/tbcload libtbcload1.7.so]];\nlappend auto_path /opt/ActiveTcl-8.6/lib/tcllib1.18;"; cat main.tbc) > tmp.tbc && mv tmp.tbc main.tbc
# RUN sed -i 's/tbcload 1.6/tbcload 1.7/g' ./main.tbc

# AND COMMENT THIS LINE
COPY main.tbc /home/chal/src/main.tbc

# Run the challenge with `tclsh main.tbc`
ENTRYPOINT [ "/bin/bash" ]