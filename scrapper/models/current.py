"""Module contains the model classes used"""
from scrapper.models.base import BaseModel


class Stock(BaseModel):
    def __init__(self, name, symbol, threshold=None):
        self.name = name
        self.symbol = symbol
        self.threshold = threshold

    def __repr__(self):
        return '<Stock(symbol={})>'.format(self.symbol)

class Bond(BaseModel):
    def __init__(self, name, isin, threshold=None):
        self.name = name
        self.isin = isin
        self.threshold = threshold

    def __repr__(self):
        return '<Bond(isin={})>'.format(self.isin)
