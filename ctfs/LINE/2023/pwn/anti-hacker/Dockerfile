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
RUN apt-get update && apt-get -y dist-upgrade && apt-get -y upgrade && apt-get -q -y install xinetd net-tools netcat sudo curl wget python3 python3-pip
RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag /
COPY loader /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:501458c0426acc3b5a74a661791271faf0dca6555b46bfb76f944d2558bd08d5

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/
RUN chmod 644 /home/user/nsjail.cfg

CMD kctf_setup && \
    kctf_drop_privs \
      socat TCP-LISTEN:9999,reuseaddr,fork \
      EXEC:"nsjail --config /home/user/nsjail.cfg -- /home/user/loader",stderr
