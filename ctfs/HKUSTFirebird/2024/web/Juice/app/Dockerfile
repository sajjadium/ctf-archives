FROM drogonframework/drogon

RUN apt-get update && \
    apt-get install -y \
    clang \
    ladspa-sdk \
    freeglut3-dev \
    g++ \
    libasound2-dev \
    libcurl4-openssl-dev \
    libfreetype6-dev \
    libjack-jackd2-dev \
    libx11-dev \
    libxcomposite-dev \
    mesa-common-dev \
    webkit2gtk-4.0

WORKDIR /app
COPY . /app

RUN mkdir build && cd build && cmake .. -D CMAKE_BUILD_TYPE=Release && make -j4

CMD ["./build/bin/webserver"]