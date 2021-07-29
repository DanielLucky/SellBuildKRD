from django.shortcuts import render
from .models import Sell, Image
from django.core.paginator import Paginator
from django.http import Http404


# def listing(request):
#     contact_list = Contact.objects.all()
#     paginator = Paginator(contact_list, 25) # Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'list.html', {'page_obj': page_obj})
#

def index(request):
    try:
        if request.method == 'GET':
            print(request.GET.get('page'))
            sells = Sell.objects.order_by('-pub_date')
            p = Paginator(sells, 10)
            if request.GET.get('page') is not None:
                page = int(request.GET.get('page'))
                return render(request, "listing.html", {"sells": p.page(page)})
            return render(request, "listing.html", {"sells": p.page(1)})
    except MyModel.DoesNotExist:
        raise Http404("No MyModel matches the given query.")



def sell(request, id_item):
    info = Sell.objects.filter(pk=id_item)
    images = Image.objects.filter(sellId=id_item)

    return render(request, "detail.html", {"sell": info, 'images': images})


