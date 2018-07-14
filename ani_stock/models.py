import datetime
import hashlib
import random

from django.db import models


# Create your models here.
def upload_stock_icon(instance, filename: str):
    ext = filename.split('.')[-1]
    # if instance.cover:
    #     game = Game.objects.get(pk=instance.id)
    #     if game.cover.name != "game_cover/game.png":
    #         os.remove(os.path.join(settings.MEDIA_ROOT, 'game_cover', game.cover.name.replace("game_cover/", "")))
    return f'stock_cover/{hashlib.md5(filename.encode()).hexdigest()}.{ext}'


class Stock(models.Model):
    code = models.CharField(max_length=12)
    circulation = models.FloatField()
    name = models.CharField(max_length=32)
    icon = models.ImageField(null=True, upload_to=upload_stock_icon)
    start_price = models.FloatField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} | {self.name}'

    '''
    stock start exchange of day
    '''

    def daily_start(self, time: datetime.datetime):
        day_time = datetime.datetime(time.year, time.month, time.day, 00, 00, 00, 00)
        # check if today data is exist
        if not StockDaily.objects.filter(time=day_time, stock_id=self.id).exists():
            random_rate = random.uniform(-0.02, 0.02)
            # check if is first day of stock
            if StockDaily.objects.filter(stock_id=self.id,time__lte=datetime.datetime.now()).count() == 0:
                StockDaily.objects.create(
                    stock_id=self.id,
                    open_price=self.start_price * (1 + random_rate),
                    close_price=None,
                    max_price=self.start_price * (1 + random_rate),
                    min_price=self.start_price * (1 + random_rate),
                    rate=0.0,
                    time=day_time
                )
            else:
                yesterday = day_time - datetime.timedelta(1)
                yesterday_stock = StockDaily.objects.filter(time=yesterday, stock_id=self.id).first()
                if yesterday_stock is not None:
                    start_price = yesterday_stock.close_price * (1 + random_rate)
                    StockDaily.objects.create(
                        stock_id=self.id,
                        open_price=start_price,
                        close_price=None,
                        max_price=start_price,
                        min_price=start_price,
                        rate=0.00,
                        time=day_time
                    )

    def daily_end(self, time):
        day_time = datetime.datetime(time.year, time.month, time.day, 00, 00, 00, 00)
        # check has log
        daily_stock: StockDaily = StockDaily.objects.filter(stock_id=self.id, time=day_time).first()
        if daily_stock is not None and daily_stock.close_price is None:
            # check has last hourly data
            last_hourly: StockHourly = StockHourly.objects.filter(
                stock_id=self.id,
                time__gte=day_time,
                time__lte=day_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
            ).order_by('-time').first()
            if last_hourly is not None:
                random_rate = random.uniform(-0.05, 0.05)
                close_price = last_hourly.price * (1 + random_rate)
                daily_stock.close_price = close_price
                daily_stock.update_rate(close_price)
                daily_stock.update_max_or_min(close_price)
                daily_stock.save()

    def add_hourly_data(self, time: datetime.datetime):
        day_time = datetime.datetime(time.year, time.month, time.day, 00, 00, 00, 00)
        hour_time = datetime.datetime(time.year, time.month, time.day, time.hour, 00, 00, 00)
        # check it has the day
        daily_stock: StockDaily = StockDaily.objects.filter(time=day_time, stock_id=self.id).first()
        if daily_stock is not None:
            # is it log  exist
            if not StockHourly.objects.filter(stock_id=self.id, time=hour_time).exists():
                random_rate = random.uniform(-0.02, 0.02)
                last_hourly_log: StockHourly = StockHourly.objects.filter(
                    stock_id=self.id,
                    time=hour_time - datetime.timedelta(hours=1)).first()
                if last_hourly_log is not None:
                    new_hourly_stock = StockHourly.objects.create(
                        stock_id=self.id,
                        price=last_hourly_log.price * (1 + random_rate),
                        time=hour_time
                    )

                    # update max of day
                    daily_stock.update_max_or_min(new_hourly_stock.price)
                    daily_stock.save()

                else:
                    # first hourly log of day
                    new_hourly_stock = StockHourly.objects.create(
                        stock_id=self.id,
                        price=daily_stock.open_price * (1 + random_rate),
                        time=hour_time
                    )

                    # update max of day
                    daily_stock.update_max_or_min(new_hourly_stock.price)
                    daily_stock.save()


class StockDaily(models.Model):
    stock = models.ForeignKey(Stock, related_name='about_stock', on_delete=models.CASCADE)
    open_price = models.FloatField()
    close_price = models.FloatField(null=True)
    max_price = models.FloatField()
    min_price = models.FloatField()
    rate = models.FloatField()
    time = models.DateTimeField()
    create = models.DateTimeField(auto_now_add=True)

    def update_max_or_min(self, price: float):
        if price > self.max_price:
            self.max_price = price
        elif price < self.min_price:
            self.min_price = price

    def update_rate(self, price: float):
        self.rate = (price - self.open_price) / self.open_price


class StockHourly(models.Model):
    stock = models.ForeignKey(Stock, related_name='hourly_about_stock', on_delete=models.CASCADE)
    price = models.FloatField()
    time = models.DateTimeField()
    create = models.DateTimeField(auto_now_add=True)

    def create_random_stock_price(self, time):
        random_rate = random.uniform(-0.02, 0.02)
        new_price = self.price * (1 + random_rate)
        return StockHourly.objects.create(stock_id=self.stock.id, price=new_price, time=time)
