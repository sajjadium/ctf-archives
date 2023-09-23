FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y xinetd
RUN apt-get install -y strace
RUN apt-get clean
RUN useradd -m user

ADD share/flag.txt /home/user/flag.txt
ADD share/challenge /home/user/challenge
ADD share/run.sh /home/user/run.sh

ADD share/libfaiss.so /home/user/libfaiss.so
ADD share/libgomp.so.1 /home/user/libgomp.so.1
ADD share/libmkl_avx512.so /home/user/libmkl_avx512.so
ADD share/libmkl_core.so /home/user/libmkl_core.so
ADD share/libmkl_intel_lp64.so /home/user/libmkl_intel_lp64.so
ADD share/libmkl_sequential.so /home/user/libmkl_sequential.so
ADD share/libmkl_def.so /home/user/libmkl_def.so

ADD xinetd /etc/xinetd.d/user

RUN chown -R user:user /home/user
RUN chown root:root /home/user/flag.txt
RUN chown user:root /home/user/challenge
RUN chmod 444 /home/user/flag.txt
RUN chmod +x /home/user/challenge
RUN chmod +x /home/user/run.sh
RUN chmod +x /home/user/libfaiss.so
RUN chmod +x /home/user/libgomp.so.1
RUN chmod +x /home/user/libmkl_avx512.so
RUN chmod +x /home/user/libmkl_core.so
RUN chmod +x /home/user/libmkl_intel_lp64.so
RUN chmod +x /home/user/libmkl_sequential.so
RUN chmod +x /home/user/libmkl_def.so

ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/home/user"

USER user
WORKDIR /home/user

EXPOSE 3088

CMD ["/usr/sbin/xinetd", "-dontfork"]