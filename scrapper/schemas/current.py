"""Schema classes for current data."""
from marshmallow import Schema, fields


class CurrentSchema(Schema):
    """Base schema with common fields and field validation for current data."""

    time = fields.DateTime()
    name = fields.String(
        required=True,
        error_messages={'required': 'Name of the asset is required.'})
    price = fields.Float()
    threshold_upper = fields.Float()
    threshold_lower = fields.Float()
    progress = fields.Float()


class StockSchema(CurrentSchema):
    """Schema for for serialization and validation of Stock objects."""

    symbol = fields.String(
        required=True,
        error_messages={'required': 'Symbol of the stock is required.'})
    variation = fields.Float()


class BondSchema(CurrentSchema):
    """Schema for for serialization and validation of Bond objects."""

    name = fields.String(
        required=True,
        error_messages={'required': 'Isin of the Bond is required.'})
    yield_y = fields.Float()
    yield_tot = fields.Float()
