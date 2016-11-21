"""Classes for the management of current data."""
from scrapper.models.base import BaseModel
from scrapper.utils import get_logger

logger = get_logger('models')


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
