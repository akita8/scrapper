from marshmallow import Schema, fields


class StockSchema(Schema):
    name = fields.Str()
    symbol = fields.Str()
