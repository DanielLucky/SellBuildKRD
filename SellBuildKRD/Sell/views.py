from django.shortcuts import render
from .models import Sell
from django.http import HttpResponse
# Create your views here.


def index(request):
    latest = Sell.objects.order_by('-pub_date')[:10]
    return render(request, "listing.html", {"sells":latest})


def sell(request, id):
    info = Sell.objects.filter(pk=id)

    return render(request, "card.html", {"sell":info})