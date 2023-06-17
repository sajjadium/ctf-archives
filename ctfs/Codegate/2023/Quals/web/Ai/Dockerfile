FROM amazoncorretto:18

RUN yum install -y shadow-utils

RUN groupadd -g 1000 ai 
RUN useradd -g ai -s /bin/bash ai

ADD ai-0.0.1-SNAPSHOT.jar /home/ai/ai-0.0.1-SNAPSHOT.jar
ADD flag.txt /flag.txt

RUN chmod 705 /home/ai/ai-0.0.1-SNAPSHOT.jar
RUN chmod 704 /flag.txt
RUN mv flag.txt flag-`md5sum flag.txt | awk '{print $1}'`.txt

RUN chown ai:ai /home/ai/ai-0.0.1-SNAPSHOT.jar

EXPOSE 8080
USER ai
WORKDIR /home/ai

CMD ["java", "-jar", "ai-0.0.1-SNAPSHOT.jar"]