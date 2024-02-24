FROM ubuntu:20.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN set -e -x; \
    apt update -y; \
    apt upgrade -y; \
	apt install -y software-properties-common; \
	apt install -y openjdk-17-jdk; \
	apt install -y unzip wget socat; \
	apt install -y cpu-checker qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager;

RUN set -e -x; \
	wget https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip -O commandlinetools.zip; \
	mkdir -p /opt/android/sdk/cmdline-tools; \
	unzip commandlinetools.zip; \
	mv tools /opt/android/sdk/cmdline-tools/latest; \
	rm commandlinetools.zip;

ENV PATH "/opt/android/sdk/cmdline-tools/latest/bin:${PATH}"
ENV ANDROID_SDK_ROOT "/opt/android/sdk"

RUN set -e -x; \
	yes | sdkmanager --install \
		"cmdline-tools;latest" \
		"platform-tools" \
		"build-tools;30.0.0" \
		"platforms;android-30" \
		"system-images;android-30;default;x86_64" \
		"emulator";

RUN sdkmanager --update;

ENV PATH "/opt/android/sdk/emulator:${PATH}"
ENV PATH "/opt/android/sdk/platform-tools:${PATH}"
ENV PATH "/opt/android/sdk/build-tools/30.0.0:${PATH}"

COPY flag script.py app.apk /chall/
RUN chmod 755 /chall/script.py
RUN chmod 644 /chall/app.apk /chall/flag

RUN mkdir /home/user/
RUN chmod 755 /home/user/

EXPOSE 1337
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/chall/script.py"
