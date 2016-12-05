"""Classes for the management of current data."""
from .base import BaseModel


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
