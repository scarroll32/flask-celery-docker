import os
import time
from celery import Celery
from celery.utils.log import get_task_logger
from celery import app
from celery.signals import task_failure
import rollbar
from flask import got_request_exception
from dotenv import load_dotenv
load_dotenv()

logger = get_task_logger(__name__)
env=os.environ
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
ROLLBAR_KEY = env.get('ROLLBAR_KEY')
ROLLBAR_APP = env.get('ROLLBAR_APP')

def celery_base_data_hook(request, data):
    data['framework'] = 'celery'

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
rollbar.init(ROLLBAR_KEY,ROLLBAR_APP)
rollbar.BASE_DATA_HOOK = celery_base_data_hook

@task_failure.connect
def handle_task_failure(**kw):
    rollbar.report_exc_info(extra_data=kw)


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    rollbar.report_message('Task ADD booted', 'warning')
    logger.info('[task] add:' + str(x) + ' + ' + str(y))
    time.sleep(5)
    return x + y


@celery.task(name='tasks.multiply')
def multiply(x: int, y: int) -> int:
    rollbar.report_message('Task MULTIPLY booted', 'warning')
    logger.info('[task] multiply:' + str(x) + ' + ' + str(y))
    w = 1 / 0
    time.sleep(5)
    return x * y
