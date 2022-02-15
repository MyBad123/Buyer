from celery import shared_task

@shared_task
def wow(wow1):
    with open('/Users/gena/Desktop/h1z.html', 'w+'):
        pass
    return wow1

