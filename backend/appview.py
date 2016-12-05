"""Application view module."""
from flask import send_from_directory
from flask.views import View


class QuasarApp(View):
    """The view that returns the angular  application."""

    def dispatch_request(self):
        """Function that sends the main app template."""
        return send_from_directory('')
