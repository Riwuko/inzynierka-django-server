from django.utils import autoreload


def run_celery():
    from server_config.celery import app

    app.worker_main(["-Aserver_config", "-linfo", "-Psolo"])


print("Starting celery worker with autoreload...")
autoreload.run_with_reloader(run_celery)
