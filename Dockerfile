FROM python:alpine

ENV TZ=Pacific/Auckland

RUN apk add -U tzdata \
    && echo ${TZ} > /etc/timezone \
    && cp /usr/share/zoneinfo/Pacific/Auckland /etc/localtime

COPY . /app
WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "app.py"]