# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
import scrapper.commands as commands


def create_app():
    """The app factory function."""
    app = Flask(__name__)
    register_commands(app)
    return app


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.mypy)
