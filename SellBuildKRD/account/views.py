from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .forms import CreateUserForm, ImageForm, ContactSendForm
from .models import ContactSend

from django.views.generic import CreateView
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"


def ContactSendView(request):
    if request.method == 'GET':
        return render(request, 'contactSend.html')
    elif request.method == 'POST':
        form = ContactSendForm(request.POST)
        if form.is_valid():
            ContactSend.objects.create(name_agent=request.user,
                                           theme=request.POST.get('theme'),
                                           message=request.POST.get('message'),)

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


@login_required(login_url='/account/login')
def agencyDetail(request):
    if request.method == 'GET':
        sellModel = apps.get_model('Sell', 'Sell')
        targets = sellModel.objects.filter(author=request.user.pk).order_by('-pk')
        return render(request, 'account/agency-detail.html', {'targets': targets})

    elif request.method == 'POST':
        Sell = apps.get_model('Sell', 'Sell')
        delete = Sell.objects.get(pk=request.POST.get('delete')).delete()

        return redirect('/account/detail')

