import _thread
import datetime

import schedule
from django.db.models import Max, Min, Avg
from django.shortcuts import render
# Create your views here.
from django.views import View

from ani_stock.models import Stock, StockDaily, StockHourly
from ani_stock.tasks import update_stock, update_open_daily_stock, close_stock


class StockView(View):
    template_name = "stock.html"

    def get(self, request, *args, **kwargs):
        stock = Stock.objects.get(pk=kwargs['stock_id'])
        last_five = StockDaily.objects.filter(stock_id=kwargs['stock_id'], time__lte=datetime.datetime.now()).order_by(
            "-create")[:5]
        for daily in last_five:
            daily.rate *= 100.0
            daily.rate = round(daily.rate, 2)
            daily.open_price = round(daily.open_price, 2)
            daily.close_price = round(daily.close_price, 2)
            daily.max_price = round(daily.max_price, 2)
            daily.min_price = round(daily.min_price, 2)
        return render(request, self.template_name, {
            'stock': stock,
            'last_five': last_five,
            'index': 'info'
        })


class StockChartView(View):
    template_name = "stock-chart.html"

    def get(self, request, *args, **kwargs):
        stock = Stock.objects.get(pk=kwargs['stock_id'])
        template_var = {
            'stock': stock,
            'index': 'now'
        }
        now = datetime.datetime.now()
        # get today
        today_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0)
        today_stock: StockDaily = StockDaily.objects.filter(time=today_date, stock_id=kwargs['stock_id']).first()
        if today_stock is not None:
            # get last hourly
            today_hourly_list = StockHourly.objects.filter(
                time__gte=today_date,
                time__lte=datetime.datetime.now(),
                stock_id=kwargs['stock_id']
            ).order_by("-time").all()
            if len(today_hourly_list) != 0:
                template_var['today_max'] = today_hourly_list.aggregate(Max("price"))['price__max']
                template_var['today_min'] = today_hourly_list.aggregate(Min("price"))['price__min']
                today_open_price = today_stock.open_price
                template_var['today_open'] = today_open_price
                last_hourly: StockHourly = today_hourly_list.last()
                template_var['today_rate'] = ((last_hourly.price - today_open_price) / today_open_price) * 100
                template_var['now_price'] = today_hourly_list.first().price
                template_var['avg_price'] = today_hourly_list.aggregate(Avg("price"))['price__avg']

        # yesterday close price
        yesterday_stock: StockDaily = StockDaily.objects.filter(
            time=today_date - datetime.timedelta(days=1),
            stock_id=kwargs['stock_id']
        ).first()
        if yesterday_stock is not None:
            template_var['yesterday_close'] = yesterday_stock.close_price

        return render(request, self.template_name, template_var)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        stock_list = Stock.objects.all().order_by("-create")[:48]
        stocks = [list(stock_list[i:i + 5]) for i in range(0, len(stock_list), 5)]
        return render(request, 'index.html', {
            'stocks': stocks
        })


def start_update_stock_task():
    _thread.start_new_thread(create_update_stock_task, ())


def create_update_stock_task():
    schedule.every().days.at('00:22').do()
    while True:
        schedule.run_pending()


# start_update_stock_task()
# update_open_daily_stock(datetime.datetime.now())
# close_stock(datetime.datetime(2018, 7, 14, 16, 0, 0, 0))


# update_stock(datetime.datetime(2018, 7, 14, 16, 0, 0, 0))

def test_stock():
    start_time = datetime.datetime(2018, 7, 1, 9, 0, 0, 0)
    for day in range(0, 240):
        update_open_daily_stock(start_time + datetime.timedelta(day))
        for hour in range(0, 7):
            update_stock(start_time + datetime.timedelta(days=day, hours=hour))
        close_stock(start_time + datetime.timedelta(day))

# test_stock()
