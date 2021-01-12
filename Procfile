release: python manage.py migrate
web: gunicorn server_config.wsgi --log-file -
worker: celery -A server_config beat -l info
celery -A server_config worker -l INFO
