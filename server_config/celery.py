from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server_config.settings")

app = Celery("server_config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
