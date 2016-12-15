"""Method views for current data."""
from flask import json, request
from flask.views import MethodView

from backend.schemas.current import BondSchema, StockSchema


class BaseAPI(MethodView):
    """Base api for current data."""

    __schema__ = None

    def check_and_serialize(self, model):
        """Method that checks if the key is in db and serializes a response."""
        serialized_data, errors = self.__schema__.dumps(model)
        if errors:
            return json.dumps(errors), 404
        return serialized_data, 200

    def get(self, key):
        """HTTP method GET."""
        if key is None:
            models = self.__schema__.model.from_db(many=True)
            if not models:
                m_type = self.__schema__.model.model_type.capitalize()
                db_err = {'database': ['{} database is empty'.format(m_type)]}
                return json.dumps(db_err), 404
            r = self.__schema__.dumps(models, many=True)

            return r.data
        else:
            m = self.__schema__.model.from_db(key)
            return self.check_and_serialize(m)

    def post(self):
        """HTTP method POST."""
        from backend.tasks import single_stock_update
        validated_model, errors = self.__schema__.load(request.form)
        if errors:
            return json.dumps(errors), 400
        validated_model.update_db()
        key = validated_model.key()
        single_stock_update.delay(key)
        return json.dumps('{} CREATED'.format(repr(validated_model))), 201

    def delete(self, key):
        """HTTP method DELETE."""
        m = self.__schema__.model.from_db(key)
        data, http_status = self.check_and_serialize(m)
        if http_status != 404:
            m.delete()
        return data, http_status


class CurrentStockAPI(BaseAPI):
    """Api for current Stock data."""

    __schema__ = StockSchema()


class CurrentBondAPI(BaseAPI):
    """Api for current Bond data."""

    __schema__ = BondSchema()
