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
FROM ubuntu:22.04

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
      ca-certificates curl python3 python-is-python3 python3-pip socat gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/user/
COPY flag main.c challenge.py /home/user/
RUN chown root:root flag main.c challenge.py 
RUN chmod 755 flag main.c challenge.py 

RUN chown user:user /home/user
RUN chmod 755 /home/user

RUN chmod a+x /home/user/challenge.py
RUN python3 -m pip install meson==1.1.1
RUN python3 -m pip install ninja

EXPOSE 1337

CMD   socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"timeout 120 python3 /home/user/challenge.py"
