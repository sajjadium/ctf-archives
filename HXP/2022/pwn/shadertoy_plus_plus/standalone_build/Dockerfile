FROM ubuntu:22.04

# Build ANGLE and dependencies for this challenge's purpose
RUN apt-get update
RUN apt-get install -y git build-essential python3 curl lsb-base lsb-release sudo file
RUN apt-get install -y --no-install-recommends python3
RUN cd / && git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
ENV PATH=/depot_tools:$PATH
RUN mkdir angle && cd angle && fetch angle

# Checkout some point of time.
# If something breaks in some other lib, checkout something close to 13th of Nov :)
RUN cd angle && git checkout 82855be3c811b01e3a1e17857ccce4b3a851a545 && cd third_party/SwiftShader && git checkout 87d41aad5e711b9c56bfd8c90b31815ac8cd299b

RUN cd angle && \
	sed -i 's/snapcraft/libjpeg-dev/' ./build/install-build-deps.sh && \
	./build/install-build-deps.sh --no-backwards-compatible --no-nacl --no-arm --no-syms --no-chromeos-fonts --no-prompt
RUN cd angle/build && git checkout -- .
RUN cd angle && gclient sync
RUN cd angle && ./build/linux/sysroot_scripts/install-sysroot.py --arch=amd64
RUN cd angle && gn gen out/Release
RUN cd angle && \
	echo "is_debug=false\nangle_assert_always_on=false\nis_component_build=false\ntarget_cpu=\"x64\"\n" >> out/Release/args.gn && \
	echo "angle_build_all=false\nangle_enable_vulkan_validation_layers=true\nbuild_angle_gles1_conform_tests=false\n" >> out/Release/args.gn
RUN cd angle && autoninja -j 6 -C out/Release

# Build fpng for creating png files from raw data
RUN git clone https://github.com/richgel999/fpng

# Build challenge
RUN mkdir /challenge
COPY main.cpp /challenge
COPY renderer.hpp /challenge
COPY build.sh /challenge
RUN cd challenge && mkdir libs && chmod +x ./build.sh && ./build.sh

# Don't use too many resources
RUN cd challenge && echo "[Processor]\nThreadCount=2\n" > ./libs/SwiftShader.ini

CMD sh

