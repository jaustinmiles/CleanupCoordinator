import celery
import os

from app import cel

# reminders.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                       CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


@cel.task
def add(x,y):
    print(x + y)
    return x + y



