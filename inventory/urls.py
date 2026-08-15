from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.stock_search, name='stock_search'),
]
