"""Flask related commands."""
import click
import pytest
from .utils import path


@click.command()
def test():
    """Run the tests."""
    rv = pytest.main([path('tests'), '--verbose'])
    exit(rv)


