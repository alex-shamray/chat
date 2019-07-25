from __future__ import absolute_import, unicode_literals

import os

import celery.signals
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'household_budget.settings')

app = Celery('household_budget')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Completely override the logging configuration with our own.
# https://github.com/celery/celery/issues/3428#issuecomment-245058020
# http://docs.celeryproject.org/en/latest/userguide/signals.html#setup-logging
@celery.signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass
