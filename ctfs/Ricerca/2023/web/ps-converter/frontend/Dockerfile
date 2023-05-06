FROM debian:bullseye-20230411

RUN apt -y update --fix-missing
RUN apt -y upgrade
RUN apt -y install socat ghostscript sudo nginx
RUN groupadd -r user && useradd -r -g user user

COPY index.html /www/index.html
COPY default.conf /etc/nginx/conf.d/default.conf
COPY run_frontend.sh /run_frontend.sh
COPY run_ps2pdf.sh /run_ps2pdf.sh
CMD /run_frontend.sh 
EXPOSE 3000
EXPOSE 5000
