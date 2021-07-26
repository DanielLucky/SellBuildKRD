from django.shortcuts import render
from .models import Sell, Image
from django.http import HttpResponse


def index(request):
    latest = Sell.objects.order_by('-pub_date')[:10]
    return render(request, "listing.html", {"sells": latest})


def sell(request, id_item):
    info = Sell.objects.filter(pk=id_item)

    images = Image.objects.filter(sellId=id_item)

    return render(request, "detail.html", {"sell": info, 'images': images})


