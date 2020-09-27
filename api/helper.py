from math import sin, cos, sqrt, atan2, radians
import requests
from order.models import Callabacks
def distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def callback(order_code, messaje):
    callbacks = Callabacks.objects.filter()
    for cb in callbacks:
        headers = {
            'content-type': "application/json",
            'x-api-key': cb.api_key,
            }
        requests.request('POST', cb.url_callback,
            headers=headers,
            json={
                "order_code": order_code,
                "action":"near",
                "message":messaje
             })