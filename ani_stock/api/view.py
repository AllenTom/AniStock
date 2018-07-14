import datetime

from rest_framework import generics
from rest_framework import pagination

from ani_stock.api.pagination import LargeResultsSetPagination
from ani_stock.api.serializers.stock_daily import StockDailySerializer
from ani_stock.api.serializers.stock_hourly import StockHourlySerializer
from ani_stock.models import StockDaily, StockHourly


class StockDailyAPIView(generics.ListAPIView):
    serializer_class = StockDailySerializer
    pagination_class = LargeResultsSetPagination
    queryset = StockDaily.objects.all()

    def get_queryset(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        daily = StockDaily.objects.all().filter(stock_id=self.kwargs['stock_id'],
                                                time__lte=datetime.datetime(yesterday.year, yesterday.month,
                                                                            yesterday.day, 23, 59, 59, 0))
        return daily


class StockHourlyAPIView(generics.ListAPIView):
    serializer_class = StockHourlySerializer
    pagination_class = LargeResultsSetPagination
    queryset = StockHourly.objects.all()

    def get_queryset(self):
        return StockHourly.objects.all().filter(stock_id=self.kwargs['stock_id'], time__lte=datetime.datetime.now())
