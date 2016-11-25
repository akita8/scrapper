"""Schema classes for current data."""
from marshmallow import Schema, fields, post_load, pre_dump, ValidationError
from scrapper.models.current import Stock, Bond


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

    @post_load
    def make_model(self, data):
        """Post load method that returns a data filled model object."""
        return self.__model__().load_data(data)


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
