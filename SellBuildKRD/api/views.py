import datetime as dt

from django.apps import apps
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from .serializers import SellSerializer, SellSerializerAdd


@api_view(['GET', 'POST'])
def get_sell(request, id_sell=None):
    if request.method == 'GET':
        Sell = apps.get_model('Sell', 'Sell')
        sell = Sell.objects.filter(pk=id_sell)
        serializer = SellSerializer(sell, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = SellSerializerAdd(data=request.data)
        if data.is_valid():
            nameSell = request.POST.get('status') + \
                       ' ' + request.POST.get('numberOf_rooms') + \
                       'к. ' + request.POST.get('type') + ' ' + request.POST.get('totalArea') + \
                       'м. ' + request.POST.get('floor').lower() + '/' + \
                       request.POST.get('totalFloor') + ' эт.'
            data.save(nameSell=nameSell, pub_date=dt.datetime.now(), author_id=request.user.pk)
            return JsonResponse({'status': 'added'}, safe=False)
        else:
            return JsonResponse(data.errors, safe=False)


@api_view(['DELETE'])
def delete_sell(request, id_sell):
    if request.method == 'DELETE':
        Sell = apps.get_model('Sell', 'Sell')
        sell = Sell.objects.filter(pk=id_sell)
        try:
            if request.user.pk == sell[0].author_id:
                sell.delete()
                return JsonResponse({'id': id_sell,
                                     'status': 'deleted'}, safe=False)
            return JsonResponse({'id': id_sell,
                                 'status': 'You are not the author.'})
        except:
            return JsonResponse({'id': id_sell,
                                 'status': 'Not found'})

class Sells_View(generics.ListAPIView):
    Sell = apps.get_model('Sell', 'Sell')
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
