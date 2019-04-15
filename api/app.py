import os
from flask import Flask
from flask import url_for
from worker import celery
import celery.states as states
import logging
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
env=os.environ
ROLLBAR_KEY = env.get('ROLLBAR_KEY')
ROLLBAR_APP = env.get('ROLLBAR_APP')

# logging
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)


# Rollbar
@app.before_first_request
def init_rollbar():
    rollbar.init(
        ROLLBAR_KEY,
        ROLLBAR_APP,
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False)
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
    rollbar.report_message('App booted', 'warning')

@app.route('/')
def index():
    app.logger.info('[route] /')
    return "<h1>Hello, world!</h1>"

@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    app.logger.info('[route] /add/' + str(param1) + '/' + str(param2))
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/multiply/<int:param1>/<int:param2>')
def multiply(param1: int, param2: int) -> str:
    app.logger.info('[route] /multiply/' + str(param1) + '/' + str(param2))
    task = celery.send_task('tasks.multiply', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    app.logger.info('[route] /check/' + task_id)
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)
