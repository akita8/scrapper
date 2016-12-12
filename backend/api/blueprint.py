"""Module that initializes the api blueprint.

It also registers different method views to a bluprint.
"""
from flask import Blueprint
from .views import CurrentStockAPI, CurrentBondAPI
# from .views import ReportStockAPI, ReportBondAPI
# from .views import TransactionStockAPI, TransactionBondAPI


api = Blueprint('api', __name__)


def register_api(view, endpoint, url, pk='key', pk_type='string'):
    """Code based on 'http://flask.pocoo.org/docs/0.11/views/'."""
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', ])
    api.add_url_rule(url, view_func=view_func, methods=['POST', ])
    api.add_url_rule('{}<{}:{}>'.format(url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


register_api(CurrentStockAPI, 'cur_stock_api', '/stock/current/')
register_api(CurrentBondAPI, 'cur_bond_api', '/bond/current/')
# register_api(ReportStockAPI, 'rep_stock_api', '/stock/report/')
# register_api(ReportBondAPI, 'rep_bond_api', '/bond/report/')
# register_api(TransactionStockAPI, 'trans_stock_api', '/stock/transaction/')
# register_api(TransactionBondAPI, 'trans_bond_api', '/bond/transaction/')
