from celery import shared_task

@shared_task
def get_tree(url):
    return '<h1>hello</h1>'

