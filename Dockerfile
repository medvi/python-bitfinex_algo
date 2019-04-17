FROM python:3.7-alpine

COPY . /app
WORKDIR /app/src

RUN adduser -H -D -u 1000 app \
    && chown -R app:app /app/* \
    && apk add mysql mysql-client \
    && pip install -r ../requirements.txt

CMD ["python", "-mbitfinex_algo"]
