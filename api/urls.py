from django.urls import path
from .services import HealthCheck, OrderStatus, Orders, OrderGeo, Info,AssignCurrier, Socket, Sender

urlpatterns = [
    path('health-check/', HealthCheck.as_view(), name="api-health-check"),
    path('order-status/', OrderStatus.as_view(), name="api-order-status"),
    path('order/', Orders.as_view(), name="api-order"),
    path('order-location/', OrderGeo.as_view(), name="api-order-location"),
    path('order/assign-currier', AssignCurrier.as_view(), name="api-assign-trak"),
    path('info/', Info.as_view(), name="api-info"),
    path('socket/', Socket.as_view(), name="api-socket"),
    path('send/sms/',Sender.as_view(), name="api-sender"),
]
