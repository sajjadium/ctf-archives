# Copyright 2020-2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:20.04 as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget git

RUN git clone https://github.com/nodejs/node.git -b v18.7.0 --depth 1

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN . /root/.nvm/nvm.sh && nvm install 18.0.0
RUN . /root/.nvm/nvm.sh && npm install -g webpack webpack-cli

COPY webpack /webpack
COPY nodejs-inspect.patch /nodejs-inspect.patch
RUN patch -d /node -p1 < /nodejs-inspect.patch

RUN bash -c 'acp() { mkdir -p /webpack/nodejs/$(dirname $1); cp /node/lib/$1.js /webpack/nodejs/$1.js; }; \
    acp internal/util/inspect; \
    acp internal/per_context/primordials; \
    acp internal/util; \
    acp internal/errors; \
    acp internal/util/types; \
    acp internal/assert; \
    acp internal/validators; \
    '

RUN . /root/.nvm/nvm.sh && cd /webpack && npx webpack

FROM alpine as chroot

RUN echo 'https://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories
RUN apk add xvfb-run firefox pciutils-libs mesa-egl mesa-dri-swrast

RUN mkdir /home/user/

COPY app /home/user/app
COPY --from=build /webpack/dist/nodejs-bundled.js /home/user/app/nodejs-bundled.js
COPY run.sh /home/user/run.sh
COPY flag /flag

RUN echo 'user:x:1000:1000::/var/tmp:/usr/sbin/nologin' >> /etc/passwd

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

# This must be done here instead of during the chroot build, because chroot build
# bind mounts these files and attempting to write to them is moot.
RUN echo 'nameserver 0.0.0.0' > /chroot/etc/resolv.conf
RUN echo '127.0.0.1 NSJAIL' >> /chroot/etc/hosts

RUN mkdir -p /chroot/proc /chroot/var/tmp

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat -v -v -v TCP-LISTEN:1337,reuseaddr,fork \
        EXEC:'kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/run.sh'
