from flask import Blueprint, render_template

frontend = Blueprint('application', __name__, template_folder='templates')


@frontend.route('/')
def application():
    return render_template()
