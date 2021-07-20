from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.apps import apps


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
    return render(request, 'account/submit.html')


@login_required(login_url='/account/login')
def agencyDetail(request):
    sellModel = apps.get_model('Sell', 'Sell')
    targets = sellModel.objects.filter(author=request.user.pk)
    return render(request, 'account/agency-detail.html', {'targets': targets})


