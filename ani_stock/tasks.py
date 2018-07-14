from __future__ import absolute_import

import datetime
import random

from django.db.models import Max, Min

from ani_stock.models import Stock, StockHourly, StockDaily


def update_stock(time: datetime.datetime):
    print("updating")
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.add_hourly_data(time)


def update_open_daily_stock(time: datetime.datetime):
    stocks = Stock.objects.all()

    for stock in stocks:
        stock.daily_start(time)


def close_stock(time: datetime.datetime):
    stocks = Stock.objects.all()

    for stock in stocks:
       stock.daily_end(time)
