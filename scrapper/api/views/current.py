"""Method views for current data."""
from flask.views import MethodView
from .utils import key_check
from scrapper.models.current import Stock, Bond
from scrapper.schemas.current import StockSchema, BondSchema


class CurrentAPI(MethodView):
    """Base api for current data."""

    __schema__ = None

    @property
    def model(self):
        """Method returns a model instance."""
        return self.schema.__model__()

    def get(self, key):
        """HTTP method GET."""
        # needs to be adapted to changes to basemodel
        keys = self.model.get_model_keys()
        s = self.__schema__()
        if key is None:
            models = []
            for key in keys:
                m = self.model.load_data(key, from_db=True)
                models.append(m)
            r = s.dump(models, many=True)
            return r.result
        else:
            m = self.model.load_data(key, from_db=True)
            r = s.dump(m)
            return r.result if not r.errors else r.errors

    def post(self):
        """HTTP method POST."""
        pass

    def delete(self, stock_key):
        """HTTP method DELETE."""
        pass

    def put(self, stock_key):
        """HTTP method PUT."""
        pass


class CurrentStockAPI(CurrentAPI):
    """Api for current Stock data."""

    __schema__ = StockSchema


class CurrentBondAPI(CurrentAPI):
    """Api for current Bond data."""

    __schema__ = BondSchema
