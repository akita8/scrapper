"""Module contains the classes used to store and serialize current data."""
from scrapper.models.base import BaseModel


class Stock(BaseModel):
    """Documentation."""

    def key(self):
        """Documentation."""
        return '{}:{}'.format(self.time.date(), self.symbol)


class Bond(BaseModel):
    """Documentation."""

    def key(self):
        """Documentation."""
        return '{}:{}'.format(self.time.date(), self.isin)
