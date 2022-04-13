import datetime
from celery import Celery

app = Celery('periodically_tasks', broker='amqp://guest@localhost//')

@app.task
def show(arg):
    with open('/Users/gena/Desktop/lollol.txt', 'a') as file:
        file.write('wow\n')

app.add_periodic_task(5, show.s(42), name='task-name')

app.conf.timezone = 'UTC'