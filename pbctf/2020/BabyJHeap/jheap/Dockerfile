FROM thekidofarcrania/chall

# Make sure locales is set to UTF8
RUN apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8


# Make sure that /usr/share/java/java-atk-wrapper.jar gets copied properly
RUN mkdir -p /usr/share/java/
COPY java-atk-wrapper.jar /usr/share/java/java-atk-wrapper.jar

RUN touch -d "2018-04-25 17:40:46.000000000 -0400" /usr/share/java/java-atk-wrapper.jar
# Otherwise we get "A jar file is not the one used while building..."
# Java is aids...

ENV LANG   C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_ALL en_US.UTF-8 

# Copy deploy stuff
COPY deploy /app

COPY flag /flag
COPY jheap.conf /etc/xinetd.d/jheap

EXPOSE 1337

CMD ["xinetd", "-dontfork"]
