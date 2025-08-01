# Copyright 2020-2025 Google LLC
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

FROM alpine AS builder

RUN apk add --no-cache git build-base bash

RUN git clone https://github.com/ocaml/ocaml /ocaml -b 5.3.0 --depth=1
WORKDIR /ocaml
RUN ./configure
RUN make -j$(nproc) world.opt && make install

RUN mkdir -p /pwn
WORKDIR /pwn
COPY nocaml.ml ./
RUN ocamlc -c nocaml.ml

FROM alpine AS chroot

RUN apk add --no-cache bash
RUN rm -rf /usr/share/apk

COPY --from=builder /usr/local/bin/ocamlc /usr/local/bin/
COPY --from=builder /usr/local/bin/ocamlrun /usr/local/bin/
COPY --from=builder /usr/local/lib/ocaml /usr/local/lib/ocaml

RUN mkdir -p /pwn

WORKDIR /pwn
COPY flag.txt go.sh ./
COPY --from=builder /pwn/nocaml.cmi /pwn/nocaml.cmo ./

FROM gcr.io/kctf-docker/challenge@sha256:9f15314c26bd681a043557c9f136e7823414e9e662c08dde54d14a6bfd0b619f

COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat TCP-LISTEN:1337,reuseaddr,fork \
        EXEC:'kctf_pow nsjail --config /home/user/nsjail.cfg --cwd /pwn -- /bin/bash /pwn/go.sh'
