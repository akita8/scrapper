import os
import click
from subprocess import call


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
def mypy():
    """Run the type check"""
    command = None  # TODO
    rv = call(command)
    if rv != 0:
        exit(rv)
