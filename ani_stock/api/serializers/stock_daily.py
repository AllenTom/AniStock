from rest_framework import serializers

from ani_stock.models import StockDaily


class StockDailySerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y/%m/%d")

    class Meta:
        fields = "__all__"
        model = StockDaily
