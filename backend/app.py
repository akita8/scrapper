"""The app module."""
from flask import Flask
from .commands import test
from .utils import make_celery
from .appview import QuasarApp
from backend.api.blueprint import api

app = Flask(__name__)

app.register_blueprint(api)
app.add_url_rule('/', view_func=QuasarApp.as_view('frontend'))

app.cli.add_command(test)

app.config.update(CELERY_BROKER_URL='redis://localhost:6379')
celery = make_celery(app)
