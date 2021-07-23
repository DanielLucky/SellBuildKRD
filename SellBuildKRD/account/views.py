from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect

from .forms import CreateUserForm, ImageForm


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
        return render(request, 'account/submit.html', {'form': form, 'formSell': formSell})
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # location = Sell.objects.create(user=request.user)
            i = 0
            sellId = Sell.objects.create(nameSell=12345, specifications=1,
                                         price=1, address=1, telephone=1,
                                         floor=1, totalFloor=1,
                                         numberOf_rooms=1, totalArea=1,
                                         livingArea=1, kitchenArea=1,
                                         furnish=1, author=request.user)
            for f in request.FILES.getlist('imageSell'):
                i += 1
                # print(i)

                data = f.read()
                photo = Image(sellId=sellId)
                print(sellId.pk)
                photo.imageSell.save(str(sellId.pk) + '/' + f.name, ContentFile(data))
                photo.save()
            return redirect('/account/submit')
        else:
            return render(request, 'account/submit.html', {'form': form})


@login_required(login_url='/account/login')
def agencyDetail(request):
    sellModel = apps.get_model('Sell', 'Sell')
    targets = sellModel.objects.filter(author=request.user.pk)
    return render(request, 'account/agency-detail.html', {'targets': targets})


