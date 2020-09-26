from django.contrib import admin
from .models import Order, Status, Callabacks, OrderTrak
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Callabacks)
class CallabacksAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderTrak)
class OrderTrakAdmin(admin.ModelAdmin):
    pass



