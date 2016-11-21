"""Method views for current data."""
from flask.views import MethodView
from scrapper.models.current import Stock


class CurrentStockAPI(MethodView):
    """Api for current Stock data."""

    def get(self, stock_key):
        if stock_key is None:
            # return a list of stocks
            pass
        elif stock_key not in Stock.model_keys():
            # return a not key not present error
            pass
        else:
            # expose a single stock
            pass

    def post(self):
        # create a new stock
        pass

    def delete(self, stock_key):
        # delete a single stock
        pass

    def put(self, stock_id):
        # update a single stock
        pass


class CurrentBondAPI(MethodView):
    """Api for current Bond data."""

    pass
