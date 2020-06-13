web: gunicorn hercules.wsgi
worker: celery -A hercules.celery worker -B --loglevel=info