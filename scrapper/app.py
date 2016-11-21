"""The app module."""
from flask import Flask
from scrapper.commands import test
from scrapper.utils import make_celery
from scrapper.api.blueprint import api
from scrapper.frontend.appview import ApplicationView


app = Flask(__name__)

app.register_blueprint(api)
app.add_url_rule('/', view_func=ApplicationView.as_view('application'))
app.cli.add_command(test)

app.config.update(CELERY_BROKER_URL='redis://localhost:6379')

celery = make_celery(app)
