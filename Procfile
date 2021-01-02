release: python manage.py migrate
web: gunicorn server_config.wsgi --log-file -
worker: celery -A devices.tasks worker -B --loglevel=info
python manage.py celeryd -v 2 -B -s celery -E -l INFO
