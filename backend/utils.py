"""Miscellaneous utility functions."""
import os
import logging
import logging.config
from celery import Celery


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
