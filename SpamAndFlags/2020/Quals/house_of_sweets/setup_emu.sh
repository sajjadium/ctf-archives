#!/bin/bash
set -euxo pipefail

apt-get -y update
apt-get dist-upgrade -y
apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    cgroup-tools \
    openjdk-8-jre-headless \
    wget \
    unzip \
    adb \
    pulseaudio \
    libgl1-mesa-glx \
    libxcomposite1 \
    libxcursor1

rm -rf /var/lib/apt/lists/* \

cd ~
git clone https://github.com/google/nsjail
make -C nsjail
mv nsjail/nsjail /bin
rm -rf nsjail

#Get android ndk to compile
wget -q https://dl.google.com/android/repository/android-ndk-r19c-linux-x86_64.zip
unzip android-ndk-r19c-linux-x86_64.zip

#Get android sdk
wget -q https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
unzip sdk-tools-linux-4333796.zip


export SDK_HOME=~/
mkdir -p ~/.android
touch ~/.android/repositories.cfg
cd $SDK_HOME/tools/bin
./sdkmanager --licenses		# accept all
echo "y" | ./sdkmanager "system-images;android-25;google_apis;arm64-v8a"
./sdkmanager "platform-tools" "platforms;android-28"
echo "no" | ./avdmanager create avd -p ~/.android/avd/cicaavd -n cicaavd -k "system-images;android-25;google_apis;arm64-v8a" #accept [no]
./sdkmanager "emulator"

#Setup the emulator once
cd $SDK_HOME/emulator
./emulator -avd cicaavd -no-audio -no-window -selinux permissive &
sleep 30
/setup_chall.sh
pkill -f "emulator"

