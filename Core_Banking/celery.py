from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core_Banking.settings')
app = Celery('Core_Banking')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    print("Hi testing Celery every minutes")


@periodic_task(run_every=(crontab(0, 0, day_of_month='1')), name="some_task", ignore_result=True)
def profit():
    print("Hi testing Celery every minutes")
