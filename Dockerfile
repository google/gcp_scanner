# Copyright 2022 Google LLC
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


FROM python:slim-bullseye

RUN mkdir /home/sa_scanner
COPY src/ /home/sa_scanner/
COPY pyproject.toml /home/sa_scanner/
COPY README.md /home/sa_scanner

WORKDIR /home/sa_scanner
RUN pip install .


ENTRYPOINT ["gcp-scanner"]
