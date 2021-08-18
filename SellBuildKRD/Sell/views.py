from django.shortcuts import render
from .models import Sell, Image
from django.core.paginator import Paginator


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
                and request.POST.get('price') == ''\
                and request.POST.get('type') == ''\
                and request.POST.get('status') == '':
            sellSearch = Sell.objects.order_by('-pub_date')

            return render(request, "listing.html", {"sells": sellSearch})
        else:
            sellSearch = Sell.objects.order_by('-pub_date').filter(district=request.POST.get('district'), price__lte=request.POST.get('price'), type=request.POST.get('type'), status=request.POST.get('status'))

            return render(request, "listing.html", {"sells": sellSearch})


def sell(request, id_item):
    info = Sell.objects.filter(pk=id_item)
    images = Image.objects.filter(sellId=id_item)

    return render(request, "detail.html", {"sell": info, 'images': images})


def page_not_found(request, exception):     # page 404
    return render(
        request,
        "page_fail/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):      # page 500
    return render(request, "page_fail/500.html", status=500)


