web: gunicorn app:app
worker: celery -A app.cel worker -l info
