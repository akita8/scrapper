"""Base schema class."""
from marshmallow import (Schema, ValidationError, fields, post_dump, post_load,
                         pre_dump, pre_load)

from backend.utils import convert


class BaseSchema(Schema):
    """Base schema with the time and key fields and pre and post methods."""

    __model__ = None

    time = fields.DateTime(
        format='%Y-%m-%d %H:%M:%S.%f',
        attribute='created_at')
    key = fields.Method('get_key')

    @property
    def model(self):
        """Method that returns a model instance."""
        return self.__model__()

    @pre_dump
    def check_key(self, model):
        """Pre dump method that raises validation error if key not in db."""
        if hasattr(model, 'no_key'):
            raise ValidationError('Key not present in db.', 'key')
        print(model.__dict__)
        return model

    @post_dump(pass_many=True)
    def envelope(self, data, many):
        """Post dump method that json encodes serialized data."""
        print(data)
        if many:
            tranformed = {el.pop('key'): el for el in data}
            return tranformed
        data.pop('key')
        return data

    @pre_load
    def convert_values(self, data):
        """Pre load method that coverts the data values to the right types."""
        return {k: convert(v) for k, v in data.items()}

    @post_load
    def make_model(self, data):
        """Post load method that returns a data filled model object."""
        return self.__model__().from_dict(data)

    def get_key(self, obj):
        """Method that returns the key field value."""
        return obj.key()
