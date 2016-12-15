"""Miscellaneous utility functions."""
import logging
import logging.config
import os
from ast import literal_eval
from datetime import datetime

from celery import Celery
from requests import get


def path(filename):
    """It returns the absolute path of a file within the project."""
    here = os.path.abspath(os.path.dirname(__file__))
    filename_path = os.path.join(here, filename)
    return filename_path


def get_logger(name):
    """Utility function that returns a configured logger."""
    logging.config.fileConfig(path('configs/logger.ini'))
    return logging.getLogger(name)


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


def compute_progress(price, limit):
    """Function that computes the progress toward the set threshold."""
    price = float(price)
    limit = float(limit)
    if not price or not limit:
        return None
    if max(price, limit) == limit:  # price<limit
        gap = limit - price
        progress = gap / price
    else:                           # limit<price
        gap = price - limit
        progress = gap / price
    return round(progress, 4)


def current_stock_values(symbol_string):
    """Function that gets stock data from yahoo finance."""
    # url for variation and price
    url = 'http://finance.yahoo.com/d/quotes.csv?s={}&f=l1p2'
    completed_url = url.format(symbol_string)
    data = get(completed_url).text.split('\n')
    # here variation and price are divided
    raw = [x.split(',') for x in data[:-1]]
    # here variation and price are converted to float
    # keeping the same data structure
    polished = list(map(
        lambda y: [
            float(y[0]),
            float(y[1].replace('"', '')[:-1])/100],
        raw))
    return polished
