"""Schema classes for current data."""
from marshmallow import fields

from backend.models.current import Bond, Stock

from .base import BaseSchema


class CurrentSchema(BaseSchema):
    """Base schema with common fields and field validation for current data."""

    name = fields.String(
        required=True,
        error_messages={'required': 'Name of the asset is required.'})
    price = fields.Float()
    threshold_upper = fields.Float()
    threshold_lower = fields.Float()
    progress_upper = fields.Float()
    progress_lower = fields.Float()


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

    isin = fields.String(
        required=True,
        error_messages={'required': 'Isin of the Bond is required.'})
    yield_y = fields.Float()
    yield_tot = fields.Float()
