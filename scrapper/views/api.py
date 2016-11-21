from flask import Blueprint
from flask.views import MethodView

stock_api = Blueprint('api/stock', __name__)
bond_api = Blueprint('api/bond', __name__)


def register_api():
    pass


class StockCurrentAPI(MethodView):
    pass


class BondCurrentAPI(MethodView):
    pass