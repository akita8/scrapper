"""Method views for current data."""
from flask import request
from flask import jsonify
from flask.views import MethodView
from backend.schemas.current import StockSchema, BondSchema


class CurrentAPI(MethodView):
    """Base api for current data."""

    # jsonify will be adapted into a decorator
    __schema__ = None

    def get(self, key):
        """HTTP method GET."""
        if key is None:
            m = self.__schema__.model.from_db(many=True)
            r = self.__schema__.dump(m, many=True)
            return jsonify(r.data)
        else:
            m = self.__schema__.model.from_db(key)
            serialized_data, errors = self.__schema__.dump(m)
            if errors:
                return jsonify(errors), 404
            return jsonify(serialized_data)

    def post(self):
        """HTTP method POST."""
        validated_model, errors = self.__schema__.load(request.form)
        if errors:
            return jsonify(errors), 400
        validated_model.update()
        return jsonify('{} CREATED'.format(repr(validated_model))), 201

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
