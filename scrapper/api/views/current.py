"""Method views for current data."""
from flask.views import MethodView
from .utils import key_check
from scrapper.models.current import Stock, Bond
from scrapper.schemas.current import StockSchema, BondSchema


class CurrentAPI(MethodView):
    """Base api for current data."""

    model_class = None
    schema_class = None

    @property
    def model(self):
        """Method returns a model instance."""
        return self.model_class()

    @property
    def schema(self):
        """Method returns a schema instance."""
        return self.model_class()

    def get(self, key):
        """HTTP method GET."""
        # maybe i can do this check directly in the schema
        keys = self.model.get_model_keys()
        passed, error = key_check(keys, key)
        if not passed:
            return error
        elif key is None:
            models = []
            for key in keys:
                m = self.model.load_data(key, from_db=True)
                models.append(m)
            # check marshmallow docs!
            s = self.schema.dump(models, many=True)
            return s.result
        else:
            m = self.model.load_data(key, from_db=True)
            s = self.schema.dump(m)
            return s.result

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

    model_class = Stock
    schema_class = StockSchema


class CurrentBondAPI(CurrentAPI):
    """Api for current Bond data."""

    model_class = Bond
    schema_class = BondSchema
