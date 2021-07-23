from django.shortcuts import render
from .models import Sell
from django.http import HttpResponse


def index(request):
    latest = Sell.objects.order_by('-pub_date')[:10]
    return render(request, "listing.html", {"sells": latest})


def sell(request, id_item):
    info = Sell.objects.filter(pk=id_item)

    return render(request, "detail.html", {"sell": info})


