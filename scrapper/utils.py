"""Miscellaneous utility functions."""
import os


def path(filename):
    """It returns the absolute path of the desired file."""
    here = os.path.abspath(os.path.dirname(__file__))
    filename_path = os.path.join(here, filename)
    return filename_path
