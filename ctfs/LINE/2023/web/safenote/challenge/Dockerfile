FROM amazoncorretto:18

RUN yum install -y shadow-utils

RUN groupadd -g 1000 safenote 
RUN useradd -g safenote -s /bin/bash safenote

ADD safenote.jar /home/safenote/safenote.jar
ADD FLAG /FLAG

RUN chmod 705 /home/safenote/safenote.jar
RUN chmod 704 /FLAG

RUN chown safenote:safenote /home/safenote/safenote.jar

EXPOSE 8080
USER safenote
CMD cd /home/safenote/; /bin/bash -c "java -jar safenote.jar"; /bin/bash
