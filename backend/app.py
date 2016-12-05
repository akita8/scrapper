"""The app module."""
from flask import Flask, url_for
from .commands import test
from .utils import make_celery
#from .appview import QuasarApp
from backend.api.blueprint import api
import urllib

app = Flask(__name__)

app.register_blueprint(api)
# app.add_url_rule('/', view_func=QuasarApp.as_view('frontend'))

app.cli.add_command(test)
app.config.update(CELERY_BROKER_URL='redis://localhost:6379')
celery = make_celery(app)

@app.route('/')
def temp():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    return str(output)
