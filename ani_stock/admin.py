from django.contrib import admin

# Register your models here.
from ani_stock.models import Stock, StockDaily, StockHourly



@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


@admin.register(StockDaily)
class StockDailyAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'time')


@admin.register(StockHourly)
class StockDailyAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'price', 'time')
