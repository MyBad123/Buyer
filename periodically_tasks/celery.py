import datetime
from celery import Celery
from .utils import MessageNumber

app = Celery('periodically_tasks', broker='amqp://guest@localhost//')


@app.task
def show(arg):
    cls_obj = MessageNumber()
    cls_obj.get_numbers()
    cls_obj.work()


app.add_periodic_task(60, show.s(42), name='task-name')

app.conf.timezone = 'UTC'