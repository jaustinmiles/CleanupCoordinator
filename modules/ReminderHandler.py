import celery
import os

from app import reminders

reminders.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                      CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@reminders.task
def add(x,y):
    return x + y