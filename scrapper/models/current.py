"""Module contains the classes used to store and serialize current data."""
from scrapper.models.base import BaseModel


class Stock(BaseModel):
    """Documentation."""

    def __init__(self, name, symbol, threshold=None, date=None):
        """Documentation."""
        super().__init__()
        self.name = name
        self.symbol = symbol
        self.threshold = threshold
        self.date = date if date else self.date

    def key(self):
        """Documentation."""
        return '{}:{}'.format(self.date, self.symbol)

    def __repr__(self):
        """Documentation."""
        return '<Stock(symbol={})>'.format(self.symbol)


class Bond(BaseModel):
    """Documentation."""

    def __init__(self, name, isin, threshold=None):
        """Documentation."""
        self.name = name
        self.isin = isin
        self.threshold = threshold

    def __repr__(self):
        """Documentation."""
        return '<Bond(isin={})>'.format(self.isin)
