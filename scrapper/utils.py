"""Miscellaneous utility functions."""
import os
import logging
import logging.config


def path(filename):
    """It returns the absolute path of a file within the project."""
    here = os.path.abspath(os.path.dirname(__file__))
    filename_path = os.path.join(here, filename)
    return filename_path


def get_logger(name):
    """Utility function that returns a configured logger."""
    logging.config.fileConfig(path('configs/logger.ini'))
    return logging.getLogger('models')
