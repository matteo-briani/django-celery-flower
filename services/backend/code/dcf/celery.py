from __future__ import absolute_import
import os
from celery import Celery
from .settings import CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcf.settings')
app = Celery('dcf', backend=CELERY_RESULT_BACKEND)

app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': CELERY_RESULT_BACKEND,
    'default_timeout': 60 * 60
  }
}


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
