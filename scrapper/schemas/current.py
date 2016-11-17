"""Module that contains schema classes for current data."""
from marshmallow import Schema, fields, validates, ValidationError
from scrapper.models.current import Stock, Bond


class CurrentSchema(Schema):
    pass


class StockSchema(Schema):
    """Schema for for serialization and validation of Stock objects."""

    time = fields.DateTime()
    name = fields.String()
    symbol = fields.String()
    tresholds = fields.List(fields.Float())
    treshold = fields.Boolean()
    price = fields.Float()
    variation = fields.Float()
    progress = fields.Float()

    @validates('tresholds')
    def treshold_validation(self, tresholds):
        """Schema validation for treshold field."""
        for elem in tresholds:
            if elem < 0:
                raise ValidationError('Treshold must be positive')


