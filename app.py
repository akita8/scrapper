"""Module needed to start the flask app and the celery worker."""
from backend.factory import create_app
app = create_app()



