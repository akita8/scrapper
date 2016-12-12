"""Classes for the management of current data."""
from backend.utils import compute_progress

from .base import BaseModel


class Stock(BaseModel):
    """Stock model class."""

    def key(self):
        """Method that defines the pattern for the stock key."""
        return '{}:{}'.format(self.time.date(), self.symbol)

    def update_current_values(self, values):
        """Function that updates price and variation and computes progress."""
        self.price, self.variation = values
        if hasattr(self, 'threshold_upper'):
            p, t = self.price, self.threshold_upper
            self.progress_upper = compute_progress(p, t)
        if hasattr(self, 'threshold_lower'):
            p, t = self.price, self.threshold_lower
            self.progress_lower = compute_progress(p, t)
        self.update_db()


class Bond(BaseModel):
    """Documentation."""

    def key(self):
        """Documentation."""
        return '{}:{}'.format(self.time.date(), self.isin)
