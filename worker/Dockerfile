FROM python:3.6-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

COPY ./worker /worker
COPY .env /worker
WORKDIR /worker

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info
