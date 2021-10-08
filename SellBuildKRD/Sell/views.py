from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Sell, Image
from django.core.paginator import Paginator
from .serializers import SellSerializer, SellSerializerAdd
import datetime as dt


def index(request):
    if request.method == 'GET':
        sells = Sell.objects.order_by('-pub_date')
        p = Paginator(sells, 10)
        if request.GET.get('page') is not None:
            page = int(request.GET.get('page'))
            return render(request, "listing.html", {"sells": p.page(page)})
        return render(request, "listing.html", {"sells": p.page(1)})
    elif request.method == 'POST':
        if request.POST.get('district') == '' \
                and request.POST.get('price') == '' \
                and request.POST.get('type') == '' \
                and request.POST.get('status') == '':
            sellSearch = Sell.objects.order_by('-pub_date')

            return render(request, "listing.html", {"sells": sellSearch})
        else:

            d = dict(request.POST)
            del d['csrfmiddlewaretoken']
            d_new = {}
            for key in d.keys():
                if d[key][0] != '':
                    d_new[key] = d[key][0]

            sellSearch = Sell.objects.all()
            for value in d_new:
                if value == 'district':
                    sellSearch = sellSearch.filter(district=d_new[value])
                elif value == 'type':
                    sellSearch = sellSearch.filter(type=d_new[value])
                elif value == 'status':
                    sellSearch = sellSearch.filter(status=d_new[value])
                elif value == 'price':
                    sellSearch = sellSearch.filter(price__lte=d_new[value])

            return render(request, "listing.html", {"sells": sellSearch.order_by('-pub_date')})


def sell(request, id_item):
    info = Sell.objects.filter(pk=id_item)
    images = Image.objects.filter(sellId=id_item)

    return render(request, "detail.html", {"sell": info, 'images': images})


def page_not_found(request, exception):  # page 404
    return render(
        request,
        "page_fail/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):  # page 500
    return render(request, "page_fail/500.html", status=500)


@api_view(['GET', 'POST'])
def get_sell(request, id_sell=None):
    if request.method == 'GET':
        sell = Sell.objects.filter(pk=id_sell)
        serializer = SellSerializer(sell, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = SellSerializerAdd(data=request.data)
        if data.is_valid():
            data.save(nameSell='123', pub_date=dt.datetime.now(), author_id=request.user.pk)
            return JsonResponse('sell is add', safe=False)
        else:
            return JsonResponse(data.errors, safe=False)
