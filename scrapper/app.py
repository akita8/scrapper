"""The app module."""
from flask import Flask
from scrapper.commands import test
from scrapper.utils import make_celery
from scrapper.views.api import stock_api, bond_api
from scrapper.views.frontend import frontend


app = Flask(__name__)

app.register_blueprint(stock_api)
app.register_blueprint(bond_api)
app.register_blueprint(frontend)

app.cli.add_command(test)

app.config.update(CELERY_BROKER_URL='redis://localhost:6379')

celery = make_celery(app)
