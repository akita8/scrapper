"""Miscellaneous utility functions."""
import os
import logging
import logging.config
from ast import literal_eval
from celery import Celery
from datetime import datetime


def path(filename):
    """It returns the absolute path of a file within the project."""
    here = os.path.abspath(os.path.dirname(__file__))
    filename_path = os.path.join(here, filename)
    return filename_path


def get_logger(name):
    """Utility function that returns a configured logger."""
    logging.config.fileConfig(path('configs/logger.ini'))
    return logging.getLogger('models')


def make_celery(app):
    """Code taken from 'http://flask.pocoo.org/docs/0.11/patterns/celery/'."""
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def convert(value, datetime_pattern='%Y-%m-%d %H:%M:%S.%f'):
    """Static method that converts strings to the proper type.

    Examples:
    '2016-11-14 11:49:09.0' --> datetime(2016, 11, 14, 11, 49, 9, 0)
    '1.0' --> 1.0
    '1' --> 1.0
    'string' --> 'string'
    "[1, 1.0, 'string']" --> [1, 1.0, 'string']
    """
    try:
        return literal_eval(value)
    except (ValueError, SyntaxError):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, datetime_pattern)
            except ValueError:
                return value
        else:
            return value
