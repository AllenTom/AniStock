"""AniStockProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from AniStockProject import settings
from ani_stock.api.view import StockDailyAPIView, StockHourlyAPIView
from ani_stock.views import StockView, StockChartView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('stock/<int:stock_id>/', StockView.as_view(), name='stock'),
    path('stock/<int:stock_id>/chart', StockChartView.as_view(), name='stock_chart'),
    path('api/stock/<int:stock_id>/', StockDailyAPIView.as_view(), name='stock'),
    path('api/stock/<int:stock_id>/hourly', StockHourlyAPIView.as_view(), name='stock')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
