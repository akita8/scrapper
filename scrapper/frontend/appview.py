"""Application view module."""
from flask import render_template
from flask.views import View


class ApplicationView(View):
    """The  view that renders the application."""

    def dispatch_request(self):
        """Function that renders the main app template."""
        return render_template('app.html')
