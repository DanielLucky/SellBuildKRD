from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .forms import CreateUserForm, ImageForm, ContactSendForm
from .models import ContactSend
import datetime as dt

from django.views.generic import CreateView
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login")  # где login — это параметр "name" в path()
    template_name = "signup.html"


def ContactSendView(request):
    if request.method == 'GET':
        return render(request, 'contactSend.html')
    elif request.method == 'POST':
        form = ContactSendForm(request.POST)
        if form.is_valid():
            ContactSend.objects.create(name_agent=request.user,
                                       theme=request.POST.get('theme'),
                                       message=request.POST.get('message'), )

            return render(request, 'thx.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/account/submit')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/account/login')

        context = {'form': form}
    return render(request, 'account/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/account/submit')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/account/submit')
            else:
                messages.info(request, 'Логин и/или пароль неверны')
        context = {}
    return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/account/login')


@login_required(login_url='/account/login')
def submitSell(request):
    Image = apps.get_model('Sell', 'Image')
    Sell = apps.get_model('Sell', 'Sell')
    form = ImageForm()

    if request.method == 'GET':
        form = ImageForm()
        formSell = Sell()
        return render(request, 'account/submit.html')
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            nameSell = request.POST.get('status') + \
                       ' ' + request.POST.get('numberOf_rooms') + \
                       'к. ' + request.POST.get('type') + ' ' + request.POST.get('totalArea') + \
                       'м. ' + request.POST.get('floor').lower() + '/' + \
                       request.POST.get('totalFloor') + ' эт.'
            sellId = Sell.objects.create(nameSell=nameSell,
                                         specifications=request.POST.get('specifications'),
                                         price=request.POST.get('price'),
                                         address=request.POST.get('address'),
                                         telephone=request.POST.get('telephone'),
                                         floor=request.POST.get('floor'),
                                         totalFloor=request.POST.get('totalFloor'),
                                         numberOf_rooms=request.POST.get('numberOf_rooms'),
                                         totalArea=request.POST.get('totalArea'),
                                         livingArea=request.POST.get('livingArea'),
                                         kitchenArea=request.POST.get('kitchenArea'),
                                         furnish=request.POST.get('furnish'),
                                         headerImage=request.FILES.get('headerImage'),
                                         type=request.POST.get('type'),
                                         status=request.POST.get('status'),
                                         author=request.user,
                                         district=request.POST.get('district'),
                                         pub_date=dt.datetime.now(),
                                         )

            for f in request.FILES.getlist('imageSell'):
                data = f.read()
                photo = Image(sellId=sellId)
                print(sellId.pk)
                photo.imageSell.save(str(sellId.pk) + '/' + f.name, ContentFile(data))
                photo.save()
            return redirect('/account/submit')
        else:
            return render(request, 'account/detail.html', {'form': form})


def submitSell_edit(request, id_item):
    Image = apps.get_model('Sell', 'Image')
    Sell = apps.get_model('Sell', 'Sell')
    # zapr = Sell.objects.filter(pk=id_item)
    # print(request.user.pk == list(zapr.values_list('author_id', flat=True))[0])
    if request.user.pk == list(Sell.objects.filter(pk=id_item).values_list('author_id', flat=True))[0]:  # Проверка автора поста перед началом редактирования объявления
        if request.method == 'GET':
            info = Sell.objects.get(pk=id_item)
            images = Image.objects.filter(sellId=id_item)
            return render(request, "account/submit_edit.html", {"sell": info, 'images': images})
        elif request.method == 'POST':
            form = ImageForm()
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                edit_item = Sell.objects.get(pk=id_item)
                if bool(request.POST.get('Delete_headerImage')):
                    edit_item.headerImage = ''
                if bool(request.POST.get('Delete_imageSell')):
                    Image.objects.filter(sellId=id_item).delete()

                if request.FILES.get('headerImage') is not None:  # NEW
                    print('request.FILES.get("headerImage") is not None')
                    edit_item.headerImage = request.FILES.get('headerImage')

                # Редактируем имя объявления
                nameSell = request.POST.get('status') + \
                           ' ' + request.POST.get('numberOf_rooms') + \
                           'к. ' + request.POST.get('type') + ' ' + request.POST.get('totalArea') + \
                           'м. ' + request.POST.get('floor').lower() + '/' + \
                           request.POST.get('totalFloor') + ' эт.'
                print(nameSell)
                print(request.POST.get('Delete_headerImage'))
                print(request.POST.get('Delete_imageSell'))
                edit_item.nameSell = nameSell
                edit_item.specifications = request.POST.get('specifications')
                edit_item.price = request.POST.get('price')
                edit_item.address = request.POST.get('address')
                edit_item.telephone = request.POST.get('telephone')
                edit_item.floor = request.POST.get('floor')
                edit_item.totalFloor = request.POST.get('totalFloor')
                edit_item.numberOf_rooms = request.POST.get('numberOf_rooms')
                edit_item.totalArea = request.POST.get('totalArea')
                edit_item.livingArea = request.POST.get('livingArea')
                edit_item.kitchenArea = request.POST.get('kitchenArea')
                edit_item.furnish = request.POST.get('furnish')
                edit_item.type = request.POST.get('type')
                edit_item.status = request.POST.get('status')
                edit_item.author = request.user
                edit_item.district = request.POST.get('district')

                edit_item.save()
                if request.FILES.get('imageSell') is not None:
                    # print('request.FILES.get("imageSell") is not None')
                    Image.objects.filter(sellId=id_item).delete()
                    for f in request.FILES.getlist('imageSell'):
                        data = f.read()
                        photo = Image(sellId=edit_item)
                        print(edit_item.pk)
                        photo.imageSell.save(str(edit_item.pk) + '/' + f.name, ContentFile(data))
                        photo.save()
                    #return redirect(f'/{edit_item.pk}')
                return redirect(f'/{edit_item.pk}')
    else:
        return redirect('/')


@login_required(login_url='/account/login', redirect_field_name=None)
def agencyDetail(request, seller):
    if request.method == 'GET':
        sellModel = apps.get_model('Sell', 'Sell')
        user_info = User.objects.get(username=seller)
        targets = sellModel.objects.filter(author=User.objects.get(username=seller).pk).order_by('-pub_date')
        return render(request, 'account/agency-detail.html', {'targets': targets, 'userinfo': user_info})

    elif request.method == 'POST':
        Sell = apps.get_model('Sell', 'Sell')
        Sell.objects.get(pk=request.POST.get('delete')).delete()

        return redirect(f'/account/detail/{seller}')


def submitSell_upp(request, id_item):
    Sell = apps.get_model('Sell', 'Sell')
    item = Sell.objects.get(pk=id_item)
    if (dt.datetime.now(dt.timezone.utc) - item.pub_date) > dt.timedelta(days=1):
        item.pub_date = dt.datetime.now(dt.timezone.utc)
        item.published_tg = False
        item.save()
        return redirect('/about/upper/')
    else:
        return redirect('/about/upper_error/')
