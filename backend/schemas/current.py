"""Schema classes for current data."""
from marshmallow import Schema, fields, post_load, pre_load, pre_dump
from marshmallow import ValidationError
from backend.models.current import Stock, Bond
from backend.utils import convert


class CurrentSchema(Schema):
    """Base schema with common fields and field validation for current data."""

    __model__ = None

    time = fields.DateTime()
    name = fields.String(
        required=True,
        error_messages={'required': 'Name of the asset is required.'})
    price = fields.Float()
    threshold_upper = fields.Float()
    threshold_lower = fields.Float()
    progress = fields.Float()

    @property
    def model(self):
        """Method returns a model instance."""
        return self.__model__()

    @pre_dump
    def check_key(self, model):
        """Pre dump method that raises validation error if key not in db."""
        if hasattr(model, 'no_key'):
            raise ValidationError('Key not present in db.', 'key')
        return model

    @pre_load
    def convert_values(self, data):
        """Pre load method that coverts the data values to the right types."""
        return {k: convert(v) for k, v in data.items()}

    @post_load
    def make_model(self, data):
        """Post load method that returns a data filled model object."""
        return self.__model__().from_dict(data)


class StockSchema(CurrentSchema):
    """Schema for for serialization and validation of Stock objects."""

    __model__ = Stock

    symbol = fields.String(
        required=True,
        error_messages={'required': 'Symbol of the stock is required.'})
    variation = fields.Float()


class BondSchema(CurrentSchema):
    """Schema for for serialization and validation of Bond objects."""

    __model__ = Bond

    name = fields.String(
        required=True,
        error_messages={'required': 'Isin of the Bond is required.'})
    yield_y = fields.Float()
    yield_tot = fields.Float()
