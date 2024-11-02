FROM python:3.13.0

COPY . /app
WORKDIR /app
EXPOSE 8000

RUN apt-get update -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip --no-cache-dir install -r requirements.txt