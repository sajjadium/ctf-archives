# Copyright 2020 Google LLC
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
FROM ubuntu:22.04 as chroot

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /
RUN apt-get update && apt-get -y dist-upgrade && apt-get -y upgrade && apt-get -yq --no-install-recommends install build-essential net-tools netcat socat wget lsb-release wget software-properties-common gnupg git

RUN wget https://apt.llvm.org/llvm.sh
RUN chmod +x llvm.sh
RUN ./llvm.sh 15

RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag /
COPY hohoql /home/user/
COPY security.dl /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

COPY libtree-sitter.so /chroot/lib/x86_64-linux-gnu
COPY libtree-sitter.so /chroot/lib/x86_64-linux-gnu/libtree-sitter.so.0

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:9000,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/hohoql"
