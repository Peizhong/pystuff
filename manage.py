#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


'''
django-admin startproject mysite
python manage.py runserver 0:8000
python manage.py startapp subscriptions
#settings.py INSTALLED_APPS use some database table
python manage.py migrate
#add new model
python manage.py makemigrations subscriptions
#check sql
python manage.py sqlmigrate subscriptions 0001
#migrate again
python manage.py migrate
'''
