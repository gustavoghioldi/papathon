from django.db import models
import requests

# Create your models here.
class Callabacks(models.Model):
    url_callback = models.URLField(max_length=200)
    api_key = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Callback"
        verbose_name_plural = "Callbacks"

class Status(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return self.name

class Order(models.Model):
    order_code        = models.CharField(max_length=12)
    seller_id         = models.EmailField(max_length=254)
    status            = models.ForeignKey(Status, on_delete=models.CASCADE)
    order_details     = models.TextField()
    client_id         = models.IntegerField()
    lat               = models.DecimalField(max_digits=18, decimal_places=8)
    log               = models.DecimalField(max_digits=18, decimal_places=8)
    shipping_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    trak_id           = models.IntegerField(default=0)
    tag               = models.CharField(max_length=50, default='')

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, *args, **kwargs):
        callbacks = Callabacks.objects.filter()
        for cb in callbacks:
            headers = {
            'content-type': "application/json",
            'x-api-key': cb.api_key,
            }
            requests.request('POST', cb.url_callback,
            headers=headers,
            json={
                "order_code": self.order_code
             })
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.order_code
    
class OrderTrak(models.Model):
    order_id       =  models.ForeignKey(Order, on_delete=models.CASCADE)
    bk_transaction =  models.CharField(max_length=90)
    class Meta:
        verbose_name = "Trak"
        verbose_name_plural = "Trak Orders"


class SocketModel(models.Model):
    socket_id=models.CharField(max_length=50)
    seller_id=models.EmailField(max_length=254)