from django.contrib import admin
from .models import Order, Status, Callabacks, OrderTrak
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code','seller_id','status','trak_id',)
    list_filter = ('seller_id','trak_id', 'status',)
    search_fields = ('order_code','seller_id', ) 

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name','code',)

@admin.register(Callabacks)
class CallabacksAdmin(admin.ModelAdmin):
    list_display = ('url_callback',)

@admin.register(OrderTrak)
class OrderTrakAdmin(admin.ModelAdmin):
    list_display = ('order_id','bk_transaction',)
    list_filter = ('order_id',)



