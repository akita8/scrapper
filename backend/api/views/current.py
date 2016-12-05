"""Method views for current data."""
from flask import request
from flask.views import MethodView
from backend.schemas.current import StockSchema, BondSchema


class CurrentAPI(MethodView):
    """Base api for current data."""

    __schema__ = None

    def get(self, key):
        """HTTP method GET."""
        if key is None:
            m = self.model.from_db(many=True)
            r = self.__schema__.dump(m, many=True)
            return r.result
        else:
            try:
                m = self.model.from_db(key)
            except KeyError as e:
                return e
            r = self.__schema__.dump(m)
            return r.result

    def post(self):
        """HTTP method POST."""
        print(request.form)

    def delete(self, key):
        """HTTP method DELETE."""
        pass

    def put(self, key):
        """HTTP method PUT."""
        pass


class CurrentStockAPI(CurrentAPI):
    """Api for current Stock data."""

    __schema__ = StockSchema()


class CurrentBondAPI(CurrentAPI):
    """Api for current Bond data."""

    __schema__ = BondSchema()
