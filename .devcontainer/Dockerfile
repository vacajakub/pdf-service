#FROM python/3.9-slim

FROM docker.ops.iszn.cz/baseimage/debian-python3:bullseye

# for tests
RUN pip install \
        httpx==0.23.0 \
        pytest


RUN apt-get update
RUN apt-get install -y --no-install-recommends \
  docker-compose