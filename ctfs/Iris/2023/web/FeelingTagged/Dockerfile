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
FROM python:3.11.1

RUN /usr/sbin/useradd -u 1000 user

RUN python3 -m pip install flask gunicorn beautifulsoup4

COPY chal.py /home/user/
COPY home.html /home/user/

EXPOSE 1337
RUN echo "cd /home/user && env WEB_CONCURRENCY=8 python3 -m gunicorn -b 0.0.0.0:1337 \"chal:app\"" > /home/user/run.sh
RUN chmod +x /home/user/run.sh
CMD ["bash", "/home/user/run.sh"]
#CMD ["bash"]
