from django.urls import path
from .services import HealthCheck, OrderStatus, Orders, OrderGeo, Info

urlpatterns = [
    path('health-check/', HealthCheck.as_view(), name="api-health-check"),
    path('order-status/', OrderStatus.as_view(), name="api-order-status"),
    path('order/', Orders.as_view(), name="api-order"),
    path('order-location/', OrderGeo.as_view(), name="api-order-location"),
    path('info/', Info.as_view(), name="api-info"),
]
