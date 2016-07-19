from __future__ import absolute_import

import os
from kombu import serialization
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FormatTools.settings')

from django.conf import settings  # noqa

app = Celery('FormatTools')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
serialization.registry._decoders.pop("application/x-python-serialize")


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))