from rest_framework import serializers

from ani_stock.models import StockHourly


class StockHourlySerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S")

    class Meta:
        fields = '__all__'
        model = StockHourly
