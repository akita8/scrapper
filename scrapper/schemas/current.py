"""Module that """
from marshmallow import Schema, fields, validates, ValidationError
from scrapper.models.current import Stock, Bond


class StockSchema(Schema):
    """Schema for for serialization and validation of Stock objects."""

    time = fields.DateTime()
    name = fields.Str()
    symbol = fields.Str()
    treshold = fields.Float()
    negative_treshold = fields.Boolean()
    price = fields.Float()
    variation = fields.Float()
    progress = fields.Float()

    @validates('symbol')
    def validate_symbol(self, symbol):
        if Stock.key_exists()
