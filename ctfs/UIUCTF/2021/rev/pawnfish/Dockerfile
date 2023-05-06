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
FROM gcr.io/kctf-docker/challenge@sha256:460914265211af5fd006c4ceb4d2628817e9645570033827cf8db136a540b54f

RUN apt-get update && apt-get install -y locales locales-all libnuma-dev
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

WORKDIR /home/user
COPY chal stockfish nn-62ef826d1a6d.nnue flag.txt ./

CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"./chal"