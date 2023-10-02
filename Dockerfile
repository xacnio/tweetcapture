FROM python:3.11.5-alpine

RUN apk add --update --update-cache\
    chromium \
    chromium-chromedriver

WORKDIR /opt

COPY requirements.txt /opt/requirements.txt

RUN pip install -r requirements.txt

COPY . /opt

RUN pip install --no-deps .

WORKDIR /app

ENTRYPOINT  ["tweetcapture", "--chromedriver", "/usr/bin/chromedriver"]