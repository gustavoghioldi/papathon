from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from order.models import Order, Status, OrderTrak, SocketModel
import json
from blockchain.services import IotaService
from .helper import distance, callback
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class HealthCheck(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status":"ok"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class Socket(View):
    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        sm = SocketModel()
        sm.socket_id = request_body['socket_id']
        sm.seller_id = request_body['seller_id']
        sm.save()
        return JsonResponse({"status":"ok"}, status=201)

    def get(self, request, *args, **kwargs):
        seller_id=request.GET.get('seller_id')
        if seller_id:
            sm = SocketModel.objects.get(seller_id=seller_id)
            return JsonResponse(model_to_dict(sm), status=200)
        else:
            return JsonResponse({"message":"parametros inexistentes"}, status=400)
        

    def delete(self, request, *args, **kwargs):
        socket_id=request.GET.get('socket_id')
        if socket_id == "all":
            sm = SocketModel.objects.all().delete()
            return JsonResponse({"delete":"all"}, status=200)
        elif socket_id:
            sm = SocketModel.objects.get(socket_id=socket_id)
            sm.delete()
            return JsonResponse({"delete":socket_id}, status=200)
        else:
            return JsonResponse({"message":"parametros inexistentes"}, status=400)
        

@method_decorator(csrf_exempt, name='dispatch')
class Info(View):
    def get(self, request, *args, **kwargs):
        status = [model_to_dict(s) for s in  Status.objects.all()]
        return JsonResponse(status,safe=False, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class OrderStatus(View):
    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body) 
        try:
            new_status = Status.objects.get(code=request_body['status_code'])
            order = Order.objects.get(order_code=request_body['order_code'])
        except Status.DoesNotExist as e:
            return JsonResponse({"message":"no existe el status {}".format(request_body['status_code'])}, status=400)
        except Order.DoesNotExist as e:
            return JsonResponse({"message":"no existe la order {}".format(request_body['order_code'])}, status=400)
        old_status = order.status.code
        order.status = new_status
        order.save()
        payload = {
            "order_code":request_body['order_code'],
            "old_status":old_status,
            "new_status":request_body['status_code']
        }
        return JsonResponse(payload, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AssignCurrier(View):
    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        try:
            order = Order.objects.get(order_code=request_body['order_code'])
        except Order.DoesNotExist as e:
            return JsonResponse({"message":"la orden {} no existe".format(request_body['order_code'])}, status=400)
        order.trak_id = request_body['trak_id']
        order.save()
        return JsonResponse(request_body, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class Orders(View):
    def get(self, request, *args, **kwargs):
        order_code = request.GET.get('order_code')
        seller_id=request.GET.get('seller_id')
        if not seller_id and order_code:
            try:
                orders = Order.objects.get(order_code=order_code)
            except Order.DoesNotExist as e:
                return JsonResponse({"message":"no existe la order {}".format(order_code)}, status=400)
            orders_json = model_to_dict(orders)
            orders_json['status_code'] = orders.status.code
        elif order_code:
            try:
                orders = Order.objects.get(seller_id=seller_id, order_code=order_code)
            except Order.DoesNotExist as e:
                return JsonResponse({"message":"no existe la order {}".format(order_code)}, status=400)
            orders_json = model_to_dict(orders)
            orders_json['status_code'] = orders.status.code
        else:
            orders = Order.objects.filter(seller_id=seller_id)
            orders_arr = [model_to_dict(x) for x in orders]
            orders_json = []
            for i,o in enumerate(orders_arr):
                o['status_code'] = orders[i].status.code
                orders_json.append(o)
        
        return JsonResponse(orders_json, safe=False,  status=200)

@method_decorator(csrf_exempt, name='dispatch')
class OrderGeo(View):
    def post(self, request, *args, **kwargs):  
        trak_id = request.GET.get('id')
        lat=request.GET.get('lat')
        lon=request.GET.get('lon')
        iota_response = IotaService.send(trak_id, lat, lon)
        orders = Order.objects.filter(trak_id=trak_id)
        
        for order in orders:
            kmtrs = distance(lat, lon, order.lat, order.log)
            if distance(lat, lon, order.lat, order.log) <= 1 and order.status.code!='COMPLETE':
                callback(order, str(kmtrs))
                
            order_trak = OrderTrak(order_id=order, bk_transaction=iota_response['bundle'].tail_transaction.hash)
            order_trak.save()
        return JsonResponse({}, status=200)

    def get(self, request, *args, **kwargs):
        order_code = request.GET.get('order_code')
        try:
            order = Order.objects.get(order_code=order_code)
        except Order.DoesNotExist as e:
            return JsonResponse({"message":"no existe la order {}".format(order_code)}, status=400)
        
        order_trak = OrderTrak.objects.filter(order_id=order)
        if order_trak.count() == 0:
            return JsonResponse({"message":"la orden no esta trakeada"}, status=400)
        resp = (IotaService.retrive(order_trak.last().bk_transaction))
        return JsonResponse(resp, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class Sender(View):
    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        print("envio de mensaje {}".format(request_body))
        return JsonResponse({"message":"mensaje enviado"}, status=200)