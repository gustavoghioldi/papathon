from django.contrib import admin
from .models import Order, Status, Callabacks, OrderTrak
import requests
from django.forms.models import model_to_dict
import json
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code','seller_id','status','trak_id',)
    list_filter = ('seller_id','trak_id', 'status',)
    search_fields = ('order_code','seller_id', ) 
    def save_model(self, request, obj, form, change):
        obj.save()
        callbacks = Callabacks.objects.filter()
        for cb in callbacks:
            json_resp = {
                "order_code": obj.order_code,
                "action":"mutation",
                "order": {
                    "order_code": obj.order_code,
                    "seller_id":obj.seller_id,
                    "order_details":obj.order_details,
                    "client_id":obj.client_id,
                    "lat":float(obj.lat),
                    "log":float(obj.log),
                    "trak_id":obj.trak_id,
                    "order_status":obj.status.code
                }
            }
            headers = {
            'content-type': "application/json",
            'x-api-key': cb.api_key,
            }
            requests.request('POST', cb.url_callback,
            headers=headers,
            json=json_resp)
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



