"""Celery tasks."""
from backend.models.current import Stock
from backend.utils import current_stock_values
from backend.utils import make_celery
celery = make_celery()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup of periodic tasks."""
    sender.add_periodic_task(30.0, global_stock_update.s())


@celery.task
def global_stock_update():
    """Task that updates every stock model with current data."""
    stocks = Stock().from_db(many=True)
    # if the db is empty the task just returns
    if not stocks:
        return 'Empty'

    symbols = '+'.join([stock.symbol for stock in stocks])
    data = current_stock_values(symbols)

    for i, stock in enumerate(stocks):
        stock.update_current_values(data[i])
    return 'Ok'


@celery.task(name='testing')
def single_stock_update(key):
    """Task tha updates a single stock model with current data."""
    stock = Stock().from_db(key)
    data = current_stock_values(stock.symbol)
    stock.update_current_values(data)
    return 'Ok'
