# web: publicmeeting/manage.py runserver "0.0.0.0:$PORT"
web: gunicorn_django -b 0.0.0.0:$PORT -w 9 -k gevent --max-requests 250 --preload publicmeeting/project/settings/__init__.py
